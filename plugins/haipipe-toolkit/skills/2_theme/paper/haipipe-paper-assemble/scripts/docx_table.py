"""docx_table.py: a parsed LaTeX table written into Word: its cell runs (raised, bold, italic), widths, header rows and
\\multicolumn merges. Moved out of latex_room_to_docx.py (over 700 lines) when cell emphasis and a left-set panel title
were added (261118). latex_room_to_docx.py runs it inside its own namespace (_load_part)."""
from __future__ import annotations

import re

def add_marked_runs(paragraph, value: str, *, size: float, bold: bool | None = None) -> None:
    """A table cell's text: its \\textsuperscript parts raised, its \\textbf and \\textit marks bold and italic runs
    (EMPHASIS_SWITCH), the rest plain; `bold` is the row's own weight (a header row)."""
    state = {"bold": bool(bold), "italic": False}
    for part in re.split(r"(\x10[^\x11]*\x11|[\x02-\x05])", value):
        if not part:
            continue
        if part in EMPHASIS_SWITCH:
            key, on = EMPHASIS_SWITCH[part]
            state[key] = on or (key == "bold" and bool(bold))
            continue
        raised = part.startswith("\x10")
        run = paragraph.add_run(part.strip("\x10\x11") if raised else part)
        set_font(run, size=size, bold=state["bold"])
        run.italic = state["italic"] or None
        if raised:
            run.font.superscript = True


def add_table(doc: Document, display: Display, title: str = "", *, compact: bool = False) -> None:
    rows = display.rows or []
    add_caption(doc, display, title, compact=compact, keep_next=True)
    if not rows:
        return
    cell_size = float(PROFILE_CONFIG.get("table_font_size", 8 if compact else 8.5))
    widths = column_widths(rows, display.spans, font_pt=cell_size)
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    set_table_geometry(table, widths, margin=60)
    if sum(widths) > 9360:                     # a wide table runs into both margins evenly
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table._tbl.tblPr.find(qn("w:tblInd")).set(qn("w:w"), "0")
    # 0.12.0 defaults (JL 261023 "why the color of the table is like this? we should not have it"; MISQ 260928 the
    # same): no colour behind header rows and horizontal rules only, as journals print tables. A profile can still
    # ask for table_borders = "grid" or a table_header_fill colour.
    if str(PROFILE_CONFIG.get("table_borders", "horizontal")).lower() == "horizontal":
        set_horizontal_borders(table)   # top, bottom and row rules, no vertical lines
    header_fill = str(PROFILE_CONFIG.get("table_header_fill", "")).strip()
    heads = min(max(1, display.header_rows), len(rows))
    keep_together = len(rows) <= 25            # a short table moves to the next page whole
    for row_index, row in enumerate(rows):
        for col_index, value in enumerate(row):
            cell = table.cell(row_index, col_index)
            cell.text = ""
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.paragraph_format.keep_with_next = keep_together and row_index < len(rows) - 1
            pending = PENDING_MARK in value
            value = value.replace(PENDING_MARK, "")
            if value.startswith(INDENT_MARK):   # a nested row: "Part 1" under "2-part model"
                paragraph.paragraph_format.left_indent = Pt(cell_size * value.count(INDENT_MARK))
                value = value.replace(INDENT_MARK, "")
            if value.startswith(CELL_LEFT):    # \\multicolumn{n}{l}: merge_spanned_cells leaves it left
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                value = value[len(CELL_LEFT):]
            add_marked_runs(paragraph, value, size=cell_size, bold=(row_index < heads))
            if pending:   # a value still to come prints on yellow, as \pending does in the PDF (JL 261023)
                set_cell_shading(cell, "FFFF00")
            if row_index < heads and header_fill:   # profile key; "" = no fill (MISQ)
                set_cell_shading(cell, header_fill)
        if row_index < heads:
            mark_header_row(table.rows[row_index])   # every header row repeats on a new page
        cant_split(table.rows[row_index])          # a row never breaks across pages
    merge_spanned_cells(table, display.spans or [], len(rows[0]))
    if display.note:
        add_rich_text(doc, display.note, MATH_STORE, size=9, line_spacing=1.0, before=3, after=8)
    else:
        doc.add_paragraph().paragraph_format.space_after = Pt(2)


def column_widths(rows: list[list[str]], spans: list[list[int]] | None, total: int = 9360,
                  minimum: int = 450, *, font_pt: float = 8.0, pad: int = 120, max_total: int = 10400) -> list[int]:
    """Column widths in twips, measured from each column's own text.

    Before 0.8.4 every column got max(900, total // n), so a 13-column table asked for
    11,700 twips on a 9,360-twip line and the last column got the negative remainder
    ("Low%" one letter per line); an even split then still broke "0.207" and "High%"
    (JL 260928 screenshots). Now a column is never narrower than its longest unbreakable
    token (a number, "94.56%") plus the cell padding; spare room goes to the columns whose
    text would otherwise wrap; and a table that cannot fit the line may run up to
    `max_total` (the official MISQ Table 1 is 10,049 twips), centred by the caller.
    A \\multicolumn header cell does not size a column.
    """
    char = font_pt * 20 * 0.55 * 1.1          # twips per character: Times ≈ 0.55 em, +10% for bold heads
    ncol = len(rows[0])
    need = [0.0] * ncol                       # longest word: must not break
    want = [0.0] * ncol                       # whole cell on one line (capped at 28 chars)
    for r, row in enumerate(rows):
        for c, text in enumerate(row):
            span = spans[r][c] if spans and r < len(spans) and c < len(spans[r]) else 1
            text = re.sub(r"[\x02-\x05\x10\x11\x14]", "", text)   # marks take no width
            if span != 1 or not text.strip():
                continue
            # Word may break a name after a letter-hyphen ("Gemini-2.5-|flash-|lite"), never inside a number
            pieces = [piece for word in text.split() for piece in re.split(r"(?<=[A-Za-z]-)", word) if piece]
            longest = max((len(piece) for piece in pieces), default=0)
            need[c] = max(need[c], longest * char + pad)
            want[c] = max(want[c], min(len(text), 28) * char + pad)
    need = [max(float(minimum), n) for n in need]
    want = [max(w, n) for w, n in zip(want, need)]
    line = float(total)
    if sum(want) <= total:                    # everything fits on one line: share the slack
        widths = [w * total / sum(want) for w in want]
    elif sum(need) <= total:                  # words fit: give the slack to cells that would wrap
        extra = [w - n for w, n in zip(want, need)]
        slack = total - sum(need)
        widths = [n + slack * e / sum(extra) for n, e in zip(need, extra)]
    else:                                     # even the words overflow: widen into the margins
        line = min(sum(need), float(max_total))
        widths = [n * line / sum(need) for n in need]
    widths = [int(w) for w in widths]
    widths[widths.index(max(widths))] += int(round(line)) - sum(widths)   # rounding goes to the widest column
    return widths


def merge_spanned_cells(table, spans: list[list[int]], ncol: int) -> None:
    """Merge each \\multicolumn{n} cell across its n columns and centre it (0.8.4); before,
    a group header such as "LM-as-a-Judge" sat in one narrow cell beside three empty ones."""
    for r, row_spans in enumerate(spans):
        if r >= len(table.rows):
            break
        for c, span in enumerate(row_spans):
            if span > 1 and c + span - 1 < ncol:
                merged = table.cell(r, c).merge(table.cell(r, c + span - 1))
                for paragraph in list(merged.paragraphs)[1:]:
                    if not paragraph.text.strip():
                        paragraph._element.getparent().remove(paragraph._element)
                for paragraph in merged.paragraphs:
                    if paragraph.alignment is None:   # a {l} span was set left by add_table
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
