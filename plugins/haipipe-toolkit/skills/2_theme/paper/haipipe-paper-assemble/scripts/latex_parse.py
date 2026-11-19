"""latex_parse.py: read the LaTeX room: balanced groups, inputs, the Bib, citations, text, tables and the event stream (parse_events).
latex_room_to_docx.py runs this file inside its own namespace (_load_part), so BIB, LATEX_ROOM and the profile come from there."""
from __future__ import annotations

import re
from pathlib import Path


def parse_group_at(text: str, start: int) -> tuple[str, int] | None:
    """Return the balanced braced group at or after ``start``."""
    pos = start
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != "{":
        return None
    depth = 0
    for index in range(pos, len(text)):
        escaped = index > 0 and text[index - 1] == "\\"
        if text[index] == "{" and not escaped:
            depth += 1
        elif text[index] == "}" and not escaped:
            depth -= 1
            if depth == 0:
                return text[pos + 1:index], index + 1
    return text[pos + 1:], len(text)


def extract_command(text: str, command: str, occurrence: int = 1) -> str:
    pattern = re.compile(r"\\" + re.escape(command) + r"\*?")
    match = None
    cursor = 0
    for _ in range(occurrence):
        match = pattern.search(text, cursor)
        if match is None:
            return ""
        cursor = match.end()
    brace = text.find("{", match.end())
    group = parse_group_at(text, brace)
    return group[0] if group else ""


def unwrap_command(text: str, command: str, arg_count: int, keep: int = -1) -> str:
    """Replace a command with one of its balanced arguments."""
    pattern = re.compile(r"\\" + re.escape(command) + r"\*?")
    cursor = 0
    while True:
        match = pattern.search(text, cursor)
        if match is None:
            return text
        pos = match.end()
        args: list[str] = []
        end = pos
        for _ in range(arg_count):
            group = parse_group_at(text, end)
            if group is None:
                args = []
                break
            value, end = group
            args.append(value)
        if not args:
            cursor = match.end()
            continue
        replacement = args[keep]
        text = text[:match.start()] + replacement + text[end:]
        cursor = match.start() + len(replacement)


def strip_comments(text: str) -> str:
    # A % inside a verbatim block is printed text (a prompt), not a TeX comment (0.8.4).
    out, pos = [], 0
    for match in VERBATIM_PATTERN.finditer(text):
        out.append(re.sub(r"(?m)(?<!\\)%[^\n]*", "", text[pos:match.start()]))
        out.append(match.group(0))
        pos = match.end()
    out.append(re.sub(r"(?m)(?<!\\)%[^\n]*", "", text[pos:]))
    return "".join(out)


def resolve_input(reference: str, current_base: Path) -> Path | None:
    raw = Path(reference.strip())
    names = [raw] if raw.suffix else [Path(str(raw) + ".tex"), raw]
    candidates: list[Path] = []
    for base in (current_base, LATEX_ROOM, ROOT):
        candidates.extend(base / name for name in names)
    for path in candidates:
        if path.is_file():
            return path.resolve()
    return None


def expand_inputs(text: str, current_base: Path, seen: set[Path] | None = None) -> str:
    seen = set() if seen is None else seen
    pattern = re.compile(r"\\input\s*\{([^}]+)\}")

    def replace(match: re.Match[str]) -> str:
        path = resolve_input(match.group(1), current_base)
        if path is None or path in seen:
            return ""
        seen.add(path)
        return "\n" + expand_inputs(path.read_text(encoding="utf-8"), path.parent, seen) + "\n"

    previous = None
    while previous != text:
        previous = text
        text = pattern.sub(replace, text)
    return text


def parse_bib(text: str) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for match in re.finditer(r"@\w+\s*\{\s*([^,]+),", text):
        key = match.group(1).strip()
        start = match.end()
        depth = 1
        index = start
        in_quote = False
        while index < len(text) and depth:
            char = text[index]
            if char == '"' and (index == 0 or text[index - 1] != "\\"):
                in_quote = not in_quote
            elif not in_quote:
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
            index += 1
        body = text[start:index - 1]
        fields: dict[str, str] = {}
        cursor = 0
        while cursor < len(body):
            field = re.search(r"(\w+)\s*=\s*", body[cursor:])
            if field is None:
                break
            name = field.group(1).lower()
            value_start = cursor + field.end()
            if value_start >= len(body):
                break
            if body[value_start] == "{":
                group = parse_group_at(body, value_start)
                if group is None:
                    break
                value, cursor = group
            elif body[value_start] == '"':
                value_end = value_start + 1
                while value_end < len(body):
                    if body[value_end] == '"' and body[value_end - 1] != "\\":
                        break
                    value_end += 1
                value = body[value_start + 1:value_end]
                cursor = value_end + 1
            else:
                value_end = body.find(",", value_start)
                if value_end < 0:
                    value_end = len(body)
                value = body[value_start:value_end]
                cursor = value_end
            fields[name] = value.strip()
            comma = body.find(",", cursor)
            cursor = len(body) if comma < 0 else comma + 1
        records[key] = fields
    return records


def reference_value(label: str, full: bool = False) -> str:
    if full and label in REF_TEXT:
        return REF_TEXT[label]
    if not full and label in REF_NUMBERS:
        return REF_NUMBERS[label]
    return REF_TEXT.get(label, label.split(":")[-1])


def author_date_style() -> bool:
    """Author-date (MISQ, apalike) instead of numbered Vancouver (JAMA and the medical
    journals). The LaTeX lane has always followed the venue through bibstyle, while
    Word emitted "[1,2]" and a numbered list for EVERY venue: a MISQ submission was
    going out with medical-journal citations (JL 260908, caught against the
    co-author's MISQ-Official-Format.docx, which is APA author-date throughout)."""
    return str(PROFILE_CONFIG.get("citation_style", "numeric")).lower() in {"author-date", "authoryear", "apalike"}


def corporate_author(author_field: str) -> str:
    """A group author braced whole in the bib ({{American Diabetes Association}}) is one name, never split into initials."""
    raw = (author_field or "").strip()
    # The bib field {{Centers for Disease Control and Prevention}} reaches here as one braced group (parse_bib drops
    # the outer pair): a group that closes only at the last character is one name, "and" included (261101).
    if raw.startswith("{") and raw.endswith("}"):
        depth = 0
        for i, ch in enumerate(raw):
            depth += (ch == "{") - (ch == "}")
            if depth == 0 and i < len(raw) - 1:
                break        # {A} and {B}: the first group closes early, two names
        else:
            return latex_to_text(raw).strip()
    if raw.startswith("{") and raw.endswith("}") and " and " not in raw:
        return latex_to_text(raw).strip()
    return ""


def surname_of(author_field: str) -> str:
    if corporate_author(author_field):
        return corporate_author(author_field)
    first = re.split(r"\s+and\s+", latex_to_text(author_field or "").strip())[0].strip()
    if not first:
        return ""
    return (first.split(",", 1)[0] if "," in first else first.split()[-1]).strip().rstrip(".")


def author_date_label(key: str) -> str:
    """(Barnett et al., 2017) · (Buchmueller and Carey, 2018) · (Soto, 2017)"""
    fields = BIB.get(key, {})
    # A group author braced whole ({{Centers for Disease Control and Prevention}}) is read on the RAW field: once
    # latex_to_text drops the braces, "and" splits it into two people and the last word becomes the surname, which
    # printed "(Control and Prevention, 2024)" and "(Services, 2025)" in the MISQ Word file (261101).
    corporate = corporate_author(fields.get("author", ""))
    people = [corporate] if corporate else [
        a for a in re.split(r"\s+and\s+", latex_to_text(fields.get("author", "")).strip())
        if a and a.lower() != "others"]
    names = [a if corporate else surname_of(a) for a in people]
    year = latex_to_text(fields.get("year", "")).strip() or "n.d."
    if not names:
        return year
    if len(names) == 1:
        who = names[0]
    elif len(names) == 2:
        who = f"{names[0]} and {names[1]}"
    else:
        who = f"{names[0]} et al."
    return f"{who}, {year}"


def citation_text(match: re.Match[str]) -> str:
    keys = [key.strip() for key in match.group(1).split(",")]
    present = [k for k in keys if k in BIB]
    for key in present:
        if key not in CITATION_NUMBERS:
            CITATION_NUMBERS[key] = len(CITATION_NUMBERS) + 1
    if not present:
        return ""
    if author_date_style():
        return "(" + "; ".join(author_date_label(k) for k in present) + ")"
    if superscript_citations():   # AMA (JAMA): superscript numbers, ranges joined, no brackets
        return "\x0e" + number_ranges([CITATION_NUMBERS[k] for k in present]) + "\x0f"
    return "[" + ",".join(str(CITATION_NUMBERS[k]) for k in present) + "]"


def narrative_citation_text(match: re.Match[str]) -> str:
    """\\citet is the narrative form: "Barnett et al. (2017) compared", never "(Barnett et al., 2017) compared", which
    the Word file printed for every \\citet (MISQ v1114 readiness review, 261114). Numbered styles fall back to the
    parenthetical form."""
    if not author_date_style():
        return citation_text(match)
    keys = [k.strip() for k in match.group(1).split(",") if k.strip() in BIB]
    for key in keys:
        CITATION_NUMBERS.setdefault(key, len(CITATION_NUMBERS) + 1)
    return "; ".join("{} ({})".format(*author_date_label(k).rsplit(", ", 1)) for k in keys)


def superscript_citations() -> bool:
    """AMA style (JAMA, JAMA IM): citations are superscript numbers, set by citation_format = "superscript"
    in the profile (JL 261023: "JAMA's author instructions" ask for superscript Arabic numerals)."""
    return str(PROFILE_CONFIG.get("citation_format", "brackets")).lower() == "superscript"


def number_ranges(numbers: list[int]) -> str:
    """[1, 2, 3, 5] -> "1-3,5" (AMA: a run of 3 or more joined by a hyphen)."""
    out, run = [], []
    for n in sorted(set(numbers)):
        if run and n == run[-1] + 1:
            run.append(n)
            continue
        if run:
            out.append(f"{run[0]}-{run[-1]}" if len(run) >= 3 else ",".join(map(str, run)))
        run = [n]
    if run:
        out.append(f"{run[0]}-{run[-1]}" if len(run) >= 3 else ",".join(map(str, run)))
    return ",".join(out)


TEX_SYMBOLS = {
    **dict(zip(
        "alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi pi rho "
        "sigma tau upsilon phi varphi chi psi omega".split(),
        "α β γ δ ϵ ε ζ η θ ϑ ι κ λ μ ν ξ π ρ σ τ υ ϕ φ χ ψ ω".split(),
    )),
    **dict(zip(
        "Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega".split(),
        "Γ Δ Θ Λ Ξ Π Σ Υ Φ Ψ Ω".split(),
    )),
    "geq": "≥", "ge": "≥", "leq": "≤", "le": "≤", "neq": "≠", "ne": "≠", "approx": "≈",
    "sim": "~", "times": "×", "pm": "±", "cdot": "·", "in": "∈", "infty": "∞",
    "to": "→", "rightarrow": "→", "leftarrow": "←", "prime": "′", "sum": "Σ",
    "log": "log", "exp": "exp", "ln": "ln", "min": "min", "max": "max",
    "degree": "°", "textendash": "–", "textemdash": "—", "ast": "*", "star": "*",
    "dagger": "†", "ddagger": "‡", "ldots": "...", "dots": "...", "cdots": "...",
}
TEX_SYMBOL = re.compile(r"\\(" + "|".join(sorted(TEX_SYMBOLS, key=len, reverse=True)) + r")(?![A-Za-z])")


PENDING_MARK = "\x12"   # \pending{x}: a value still to come, kept as a mark so add_table shades its cell (0.12.0)
INDENT_MARK = "\x13"    # one per em of a cell's leading \hspace*, so add_table indents the cell (0.14.4)

# Layout codes carry numbers, not words. The generic stripper in latex_to_text takes only the command's name, so their
# arguments printed: "=2em=11emLinear", "1em2-part model", "1.9in Primary" (pp-LBP-JAMA 261103).
LAYOUT_ASSIGNMENT = re.compile(
    r"\\(?:hangindent|hangafter|leftskip|rightskip|parindent|parskip|hsize|baselineskip)\b"
    r"\s*=?\s*-?[\d.]*\s*(?:em|ex|in|pt|cm|mm|bp)?")
LAYOUT_COMMAND = re.compile(
    r"\\(?:[hv]space\*?\s*\{[^{}]*\}|renewcommand\s*\{[^{}]*\}\s*\{[^{}]*\}|setlength\s*\{[^{}]*\}\s*\{[^{}]*\}|addtolength\s*\{[^{}]*\}\s*\{[^{}]*\}"
    r"|rule(?:\[[^\]]*\])?\s*\{[^{}]*\}\s*\{[^{}]*\})")
MINIPAGE = re.compile(r"\\begin\{minipage\}(?:\[[^\]]*\])*(?:\{[^{}]*\})?|\\end\{minipage\}")
TRUE_MINUS = re.compile(r"(?<![\w.,/)%\u2013\u2014\u2212-])-(?=\.?\d)")


def strip_layout(value: str) -> str:
    """Drop the layout commands whose arguments are measurements; \\parbox keeps its text and loses its width."""
    value = re.sub(r"\\parbox\s*(?:\[[^\]]*\])*", r"\\parbox", value)
    value = unwrap_command(value, "parbox", 2, 1)
    value = MINIPAGE.sub("", value)
    value = LAYOUT_ASSIGNMENT.sub("", value)
    return LAYOUT_COMMAND.sub("", value)


def true_minus(value: str) -> str:
    """A hyphen that opens a number is a minus sign ("-2.5", "(-3.1 to -0.5)"); "2016-2019" and "ICD-10" keep theirs."""
    return TRUE_MINUS.sub("\u2212", value)


def unwrap_sqrt(value: str) -> str:
    """\\sqrt{x} as text, for the places that cannot hold an equation (a caption, a table cell)."""
    pattern = re.compile(r"\\sqrt\s*(?:\[[^\]]*\])?\s*(?=\{)")
    while (match := pattern.search(value)) is not None:
        group = parse_group_at(value, match.end())
        if group is None:
            return value
        value = value[:match.start()] + "\u221a(" + group[0] + ")" + value[group[1]:]
    return value


def latex_to_text(value: str) -> str:
    value = strip_layout(value or "")
    value = unwrap_sqrt(value)
    value = re.sub(r"\\pending\{([^{}]*)\}", lambda m: PENDING_MARK + m.group(1) + PENDING_MARK, value)
    value = re.sub(r"\\providecommand\{\\pending\}(\[\d\])?\{[^\n]*\}", "", value)
    value = re.sub(r"\\citet(?:\[[^\]]*\])?\{([^}]+)\}", narrative_citation_text, value)   # Author et al. (2017)
    value = re.sub(r"\\cite(?:p|t)?(?:\[[^\]]*\])?\{([^}]+)\}", citation_text, value)
    value = re.sub(
        r"\\(?:cref|Cref)\{([^}]+)\}",
        lambda m: ", ".join(reference_value(label.strip(), full=True) for label in m.group(1).split(",")),
        value,
    )
    value = re.sub(r"\\ref\{([^}]+)\}", lambda m: reference_value(m.group(1)), value)
    value = re.sub(r"\\nameref\{([^}]+)\}", lambda m: reference_value(m.group(1), full=True), value)

    value = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", value)
    value = re.sub(r"\\textsuperscript\{2\}", "²", value)
    for command, count, keep in (
        ("textcolor", 2, 1),
        ("href", 2, 1),
        ("multicolumn", 3, 2),
        ("multirow", 3, 2),
        ("resizebox", 3, 2),
        ("makecell", 1, 0),
    ):
        value = unwrap_command(value, command, count, keep)
    for command in (
        "textbf", "textit", "emph", "underline", "textrm", "textsf", "texttt",
        "textsc", "mbox", "mathrm", "mathbf", "operatorname", "text", "intertext",
        "textsuperscript", "textsubscript", "footnote", "thanks",
    ):
        value = unwrap_command(value, command, 1, 0)

    value = re.sub(r"\\textsubscript\{([^{}]*)\}", r"_\1", value)
    value = re.sub(r"\\url\{([^}]*)\}", r"\1", value)
    value = re.sub(r"\\todo\{([^{}]*)\}", r"[TODO: \1]", value)
    value = value.replace(r"\nvzq", "[not independently verified]")
    value = re.sub(r"\\label\{[^}]*\}", "", value)
    value = re.sub(r"\\(?:small|footnotesize|scriptsize|normalsize|large|Large|maketitle|clearpage|newpage|noindent|centering|raggedright)\b", "", value)

    # Convert the small set of TeX accent and annotation forms that occur in
    # the manuscript before the generic command stripper runs.  These are
    # formatting tokens, not alternate manuscript text.
    accent_map = {
        "a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú",
        "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú",
        "n": "ñ", "N": "Ñ", "c": "ç", "C": "Ç",
    }
    for letter, accented in accent_map.items():
        value = value.replace(r"\'{" + letter + "}", accented)
        value = value.replace(r"\'" + letter, accented)

    value = re.sub(r"\\[\"`~^]([A-Za-z])", lambda m: m.group(1), value)
    value = re.sub(r"\\c\{([^{}]*)\}", r"\1", value)
    value = re.sub(r"\^\s*\{([^{}]*)\}", r"\1", value)

    # Symbols match as whole command names, so \mu never eats the front of a
    # longer command. A name missing here is DROPPED by the generic stripper
    # below; that is how a table header printed "HDLD ( pp)" for "HDLD (\Delta pp)".
    value = TEX_SYMBOL.sub(lambda m: TEX_SYMBOLS[m.group(1)], value)
    replacements = {
        "~": " ", r"\&": "&", r"\%": "%", r"\_": "_", r"\#": "#", r"\$": "\ue000",   # a literal dollar survives the math-mode strip below
        r"\ ": " ", r"\,": " ", r"\;": " ", r"\!": " ",
        "``": '"', "''": '"', "---": "—", "--": "–",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", "", value)
    value = value.replace("{", "").replace("}", "").replace("$", "").replace("\ue000", "$")   # "\$134.5" printed "\134.5" (JL 261023)
    value = value.replace("^2", "²").replace("^3", "³")
    value = value.replace("kg/m2", "kg/m²")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def register_labels(text: str) -> None:
    for match in re.finditer(
        r"\\(?:section|subsection|subsubsection)\*?\s*\{([^{}]+)\}\s*\\label\{([^}]+)\}", text
    ):
        REF_TEXT[match.group(2)] = latex_to_text(match.group(1))

    counters = {"table": 0, "figure": 0}
    pattern = re.compile(r"\\begin\{(figure\*?|table\*?)\}.*?\\end\{\1\}", re.S)
    appendix = re.search(r"\\appendix\b", text) if per_appendix_numbering() else None
    main_part = text[:appendix.start()] if appendix else text
    # A \setcounter{table}{0} (JAMA's supplement restarts at eTable 1 after the references) restarts the count
    # here too, so a \ref in the Word copy prints the number the LaTeX lane prints.
    reset = re.compile(r"\\setcounter\{(table|figure)\}\{0\}")
    events = sorted([(m.start(), "reset", m.group(1)) for m in reset.finditer(main_part)]
                    + [(m.start(), "float", m) for m in pattern.finditer(main_part)], key=lambda e: e[0])
    for _, what, match in events:
        if what == "reset":
            counters[match] = 0
            continue
        kind = "figure" if match.group(1).startswith("figure") else "table"
        label = extract_command(match.group(0), "label")
        if not label:
            continue
        counters[kind] += 1
        REF_NUMBERS[label] = str(counters[kind])
        REF_TEXT[label] = f"{kind.title()} {counters[kind]}"
    if appendix is None:
        return
    # 0.8.2: after \appendix every numbered \section is a lettered appendix, and its
    # floats restart at 1 under that letter, exactly as the LaTeX lane's \counterwithin*.
    token = re.compile(r"\\section\s*\{|\\begin\{(figure\*?|table\*?)\}.*?\\end\{\1\}", re.S)
    letter, local = -1, {"table": 0, "figure": 0}
    for match in token.finditer(text[appendix.end():]):
        if match.group(1) is None:
            letter, local = letter + 1, {"table": 0, "figure": 0}
            continue
        kind = "figure" if match.group(1).startswith("figure") else "table"
        label = extract_command(match.group(0), "label")
        if not label:
            continue
        local[kind] += 1
        number = f"{chr(ord('A') + max(letter, 0))}{local[kind]}"
        REF_NUMBERS[label] = number
        REF_TEXT[label] = f"{kind.title()} {number}"


def per_appendix_numbering() -> bool:
    """0.8.2: `appendix_float_numbering = "per-appendix"` numbers appendix floats
    Table A1 … B1 …, restarting in each lettered appendix (the MISQ convention)."""
    return str(PROFILE_CONFIG.get("appendix_float_numbering", "continuous")).lower() == "per-appendix"


def find_asset(reference: str) -> Path | None:
    ref = Path(reference.strip())
    candidates: list[Path] = []
    if ref.suffix:
        candidates.extend([LATEX_ROOM / ref, LATEX_ROOM / "displays" / ref])
        candidates.extend([p.with_suffix(".png") for p in (LATEX_ROOM / ref, LATEX_ROOM / "displays" / ref)])
    else:
        for ext in (".png", ".jpg", ".jpeg", ".pdf"):
            candidates.extend([LATEX_ROOM / (str(ref) + ext), LATEX_ROOM / "displays" / (str(ref) + ext)])
    for path in candidates:
        if path.is_file():
            return path.resolve()
    stem = ref.stem
    matches = [
        path for path in LATEX_ROOM.rglob("*")
        if path.is_file() and path.stem == stem and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf"}
    ]
    matches.sort(key=lambda path: ({".png": 0, ".jpg": 1, ".jpeg": 2, ".pdf": 3}.get(path.suffix.lower(), 9), str(path)))
    return matches[0].resolve() if matches else None


_load_part("latex_table.py")   # TABULAR_BEGIN, parse_table_rows, parse_table_spans, count_header_rows, math_scripts_raised


def display_note(value: str) -> str:
    """A note under a display: its $...$ stay equations (the \\sqrt printed nothing once flattened), its minus signs true."""
    return true_minus(latex_to_text(mark_emphasis(protect_math(value, MATH_STORE))).strip())


def parse_display(block: str) -> Display:
    is_figure = bool(re.search(r"\\includegraphics(?:\[[^]]*\])?\{", block))
    caption = extract_command(block, "caption") or extract_command(block, "caption*")
    bold = re.match(r"\s*\{?\s*\\textbf\s*(?=\{)", caption)
    heading = latex_to_text(parse_group_at(caption, bold.end())[0]) if bold else ""
    label = extract_command(block, "label")
    notes = re.findall(r"\\begin\{flushleft\}(.*?)\\end\{flushleft\}", block, re.S)
    note = " ".join(display_note(n) for n in notes if latex_to_text(n).strip())
    if is_figure:
        image_match = re.search(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", block)
        image_ref = image_match.group(1) if image_match else ""
        return Display(
            kind="figure",
            block=block,
            caption=latex_to_text(caption),
            label=label,
            image_ref=image_ref,
            image_path=find_asset(image_ref) if image_ref else None,
            note=note,
            heading=heading,
        )
    # A table note sits after the tabular in \begin{flushleft}...\end{flushleft}; the PDF
    # printed it and Word dropped it until 0.8.4 (JL 260928, MISQ official format has "Note." paragraphs).
    notes = re.findall(r"\\begin\{flushleft\}(.*?)\\end\{flushleft\}", block, re.S)
    # 0.12.0: a note set in \parbox{\linewidth}{...} after the tabular (frame_displays.py writes this) was dropped too
    end = max(block.rfind("\\end{tabular}"), block.rfind("\\end{tabularx}"))
    if end >= 0:
        for m in re.finditer(r"\\parbox(?:\[[^]]*\])?", block[end:]):
            width = parse_group_at(block, end + m.end())
            body = parse_group_at(block, width[1]) if width else None
            if body:
                notes.append(re.sub(r"\\(?:footnotesize|small|scriptsize|raggedright)\b", "", body[0]))
    note = " ".join(display_note(n) for n in notes if latex_to_text(n).strip())
    return Display(kind="table", block=block, caption=latex_to_text(caption), label=label,
                   rows=parse_table_rows(block), note=note, spans=parse_table_spans(block),
                   header_rows=count_header_rows(block), heading=heading)


DISPLAY_PATTERN = re.compile(r"\\begin\{(figure\*?|table\*?)\}.*?\\end\{\1\}", re.S)
LIST_PATTERN = re.compile(r"\\begin\{(itemize|enumerate)\}.*?\\end\{\1\}", re.S)
CENTER_PATTERN = re.compile(r"\\begin\{center\}.*?\\end\{center\}", re.S)
TOKEN_PATTERN = re.compile(r"@@(?:DISPLAY|LIST|CODE)\d+@@")
# verbatim-like blocks keep their lines exactly; group 2 is the body (0.8.4)
VERBATIM_PATTERN = re.compile(r"\\begin\{(verbatim\*?|Verbatim|lstlisting)\}(?:\[[^\]]*\])?[ \t]*\n?(.*?)\\end\{\1\}", re.S)


def list_items(block: str) -> list[str]:
    body = re.sub(r"\\begin\{(?:itemize|enumerate)\}|\\end\{(?:itemize|enumerate)\}", "", block)
    return [latex_to_text(match.group(1)) for match in re.finditer(r"\\item\s*(.*?)(?=\\item|$)", body, re.S) if latex_to_text(match.group(1))]


def parse_events(text: str) -> tuple[list[Event], list[Display]]:
    blocks: dict[str, tuple[str, str]] = {}

    # First, before any other rewrite: a verbatim block is printed exactly as written
    # (JL 260928 appendix screenshot: the published prompt reached Word as double-spaced
    # prose, lines joined and the word "verbatim" printed).
    def store_code(match: re.Match[str]) -> str:
        token = f"@@CODE{len(blocks)}@@"
        blocks[token] = ("code", match.group(2))
        return "\n" + token + "\n"

    text = VERBATIM_PATTERN.sub(store_code, text)
    text = re.sub(r"\\(?:clearpage|newpage|pagebreak)\b", "\n", text)
    text = re.sub(r"\\(?:maketitle|thispagestyle|pagestyle)\s*(?:\{[^}]*\})?", "", text)
    text = re.sub(r"\\(?:bibliographystyle|bibliography)\s*(?:\{[^}]*\})?", "", text)
    # Counter and naming declarations control TeX's rendering; they are not
    # manuscript prose and must not leak into a Word projection.
    text = re.sub(r"(?m)^\s*\\(?:setcounter|renewcommand)\b.*$", "", text)
    text = re.sub(r"\\(?:begin|end)\{(?:document|abstract)\}", "", text)
    displays: list[Display] = []
    lists: list[list[str]] = []

    def store_display(match: re.Match[str]) -> str:
        token = f"@@DISPLAY{len(blocks)}@@"
        blocks[token] = ("display", match.group(0))
        return "\n" + token + "\n"

    text = DISPLAY_PATTERN.sub(store_display, text)

    def store_center(match: re.Match[str]) -> str:
        block = match.group(0)
        if "tabular" not in block and "includegraphics" not in block:
            return block
        token = f"@@DISPLAY{len(blocks)}@@"
        blocks[token] = ("display", block)
        return "\n" + token + "\n"

    text = CENTER_PATTERN.sub(store_center, text)

    def store_list(match: re.Match[str]) -> str:
        token = f"@@LIST{len(blocks)}@@"
        blocks[token] = ("list", match.group(0))
        return "\n" + token + "\n"

    text = LIST_PATTERN.sub(store_list, text)

    ordered: list[Event] = []
    heading_pattern = re.compile(r"\\(section|subsection|subsubsection|paragraph)\*?\s*")

    def add_ordered_plain(value: str) -> None:
        value = re.sub(r"\\appendix\b", "", value)
        value = re.sub(r"\\(?:begin|end)\{(?:center|table\*?|figure\*?)\}", "", value)
        for paragraph in re.split(r"\n\s*\n+", value):
            # 0.8.4: a display equation becomes its own "math" event (a native Word equation);
            # inline $…$ is kept as a @@MATHn@@ token so add_rich_text can write it as OMML.
            pos = 0
            for match in DISPLAY_MATH.finditer(paragraph):
                before = latex_to_text(mark_emphasis(protect_math(paragraph[pos:match.start()], MATH_STORE)))
                if before:
                    ordered.append(Event("text", before))
                ordered.append(Event("math", match.group(1) or match.group(2) or match.group(4) or ""))
                pos = match.end()
            rest = latex_to_text(mark_emphasis(protect_math(paragraph[pos:], MATH_STORE)))
            if rest:
                ordered.append(Event("text", rest))

    def add_before_tokens(value: str) -> None:
        parts = re.split(r"(@@(?:DISPLAY|LIST|CODE)\d+@@)", value)
        for part in parts:
            if not part:
                continue
            if part in blocks:
                kind, block = blocks[part]
                if kind == "code":
                    ordered.append(Event("code", block))
                elif kind == "list":
                    ordered.append(Event("list", list_items(block)))
                else:
                    display = parse_display(block)
                    displays.append(display)
                    ordered.append(Event("display", display))
            else:
                add_ordered_plain(part)

    cursor = 0
    while True:
        match = heading_pattern.search(text, cursor)
        if match is None:
            add_before_tokens(text[cursor:])
            break
        add_before_tokens(text[cursor:match.start()])
        brace = text.find("{", match.end())
        group = parse_group_at(text, brace)
        if group is None:
            cursor = match.end()
            continue
        title, cursor = group
        level = {"section": 1, "subsection": 2, "subsubsection": 3, "paragraph": 3}[match.group(1)]
        ordered.append(Event("heading", latex_to_text(title), level))
    return ordered, displays
