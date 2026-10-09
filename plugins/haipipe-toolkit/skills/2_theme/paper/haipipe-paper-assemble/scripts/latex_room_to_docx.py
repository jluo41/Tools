"""Build a complete paper from a configured LaTeX desk room.

This is the initial reusable ``latex-room`` adapter for
``haipipe-paper-assemble``. The paper-specific configuration is supplied by
the ``HAIPIPE_PAPER_BUILD_CONFIG`` environment variable, so the same engine
can serve multiple paper rooms. No DOCX is used as an input.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import shutil
import subprocess
import os
import tomllib
from typing import Iterable

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


CONFIG_ENV = os.environ.get("HAIPIPE_PAPER_BUILD_CONFIG")
CONFIG_PATH = (
    Path(CONFIG_ENV).expanduser().resolve()
    if CONFIG_ENV
    else Path(__file__).resolve().with_name("paper-build.toml")
)
WORD_ROOM = CONFIG_PATH.parent
ROOT = WORD_ROOM.parent
SKILL_ROOT = Path(__file__).resolve().parent.parent
PROFILE_ROOT = SKILL_ROOT / "profiles"


def load_config() -> dict[str, object]:
    if not CONFIG_PATH.exists():
        return {}
    return tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))


BUILD_CONFIG = load_config()
PAPER_CONFIG = BUILD_CONFIG.get("paper", {})
PROFILE_NAME = str(PAPER_CONFIG.get("venue_profile", "")) if isinstance(PAPER_CONFIG, dict) else ""


def load_shared_profile(name: str) -> dict[str, object]:
    """Load venue behaviour from the skill, never manuscript content from a paper."""
    if not name:
        return {}
    path = PROFILE_ROOT / f"{name}.toml"
    if not path.exists():
        raise FileNotFoundError(f"Venue profile not found: {path}")
    return tomllib.loads(path.read_text(encoding="utf-8"))


SHARED_PROFILE = load_shared_profile(PROFILE_NAME)
PAPER_PROFILE = BUILD_CONFIG.get("profile", {})
if not isinstance(PAPER_PROFILE, dict):
    raise TypeError("[profile] must be a TOML table")
PROFILE_CONFIG = {**SHARED_PROFILE, **PAPER_PROFILE}
SOURCE_CONFIG = BUILD_CONFIG.get("source", {})
OUTPUT_CONFIG = BUILD_CONFIG.get("outputs", {})
EVIDENCE_CONFIG = BUILD_CONFIG.get("evidence", {})
if not isinstance(SOURCE_CONFIG, dict) or not isinstance(OUTPUT_CONFIG, dict) or not isinstance(EVIDENCE_CONFIG, dict):
    raise TypeError("[source], [outputs], and [evidence] must be TOML tables")
LATEX_ROOM = (WORD_ROOM / Path(str(SOURCE_CONFIG.get("room", ".")))).resolve()
SECTION_DIR = LATEX_ROOM / str(SOURCE_CONFIG.get("sections", "sections"))
DISPLAY_DIR = LATEX_ROOM / str(SOURCE_CONFIG.get("displays", "displays"))
MASTER = LATEX_ROOM / str(SOURCE_CONFIG.get("master", "main.tex"))
BIB_PATH = LATEX_ROOM / str(SOURCE_CONFIG.get("bibliography", "reference.bib"))


def output_path(key: str, default: str) -> Path:
    value = Path(str(OUTPUT_CONFIG.get(key, default)))
    return value if value.is_absolute() else WORD_ROOM / value


MAIN_PATH = output_path("main_docx", "manuscript-submission-draft.docx")
SUPP_PATH = output_path("supplement_docx", "manuscript-online-supplement-draft.docx")
MAIN_PDF_PATH = output_path("main_pdf", MAIN_PATH.with_suffix(".pdf").name)
SUPP_PDF_PATH = output_path("supplement_pdf", SUPP_PATH.with_suffix(".pdf").name)
DRAFT_SECTION_ROOM = output_path("section_snapshots", "draft-sections")
ASSET_DIR = output_path("assets", "submission-assets")
MANIFEST_PATH = output_path("manifest", "build-manifest.json")
RUNNING_TITLE_FALLBACK = str(
    PROFILE_CONFIG.get(
        "running_title_fallback",
        "",
    )
)

FONT = str(PROFILE_CONFIG.get("font", "Arial"))
CITATION_NUMBERS: dict[str, int] = {}
REF_NUMBERS: dict[str, str] = {}
REF_TEXT: dict[str, str] = {}
BIB: dict[str, dict[str, str]] = {}


@dataclass
class Display:
    kind: str
    block: str
    caption: str = ""
    label: str = ""
    rows: list[list[str]] | None = None
    image_ref: str = ""
    image_path: Path | None = None
    note: str = ""          # the float's \begin{flushleft} note, printed under a Word table (0.8.4)
    spans: list[list[int]] | None = None   # \multicolumn spans aligned with rows (0.8.4)
    header_rows: int = 1                   # rows above the first \midrule (0.8.4)


@dataclass
class Event:
    kind: str
    value: str | list[str] | Display
    level: int = 0


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


def surname_of(author_field: str) -> str:
    first = re.split(r"\s+and\s+", latex_to_text(author_field or "").strip())[0].strip()
    if not first:
        return ""
    return (first.split(",", 1)[0] if "," in first else first.split()[-1]).strip().rstrip(".")


def author_date_label(key: str) -> str:
    """(Barnett et al., 2017) · (Buchmueller and Carey, 2018) · (Soto, 2017)"""
    fields = BIB.get(key, {})
    people = [a for a in re.split(r"\s+and\s+", latex_to_text(fields.get("author", "")).strip())
              if a and a.lower() != "others"]
    names = [surname_of(a) for a in people]
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
    return "[" + ",".join(str(CITATION_NUMBERS[k]) for k in present) + "]"


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


def latex_to_text(value: str) -> str:
    value = value or ""
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
        "~": " ", r"\&": "&", r"\%": "%", r"\_": "_", r"\#": "#",
        r"\ ": " ", r"\,": " ", r"\;": " ", r"\!": " ",
        "``": '"', "''": '"', "---": "—", "--": "–",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", "", value)
    value = value.replace("{", "").replace("}", "").replace("$", "")
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
    for match in pattern.finditer(main_part):
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
    span = 1
    m = re.match(r"\s*\\multicolumn\s*\{\s*(\d+)\s*\}", cell)
    if m:
        span = int(m.group(1))
        g1 = parse_group_at(cell, m.end())          # the column spec
        g2 = parse_group_at(cell, g1[1]) if g1 else None
        cell = g2[0] if g2 else cell
    # \shortstack{a\\b} stacks lines inside ONE cell; keep it one cell
    while True:
        m2 = re.search(r"\\shortstack(?:\[[^\]]*\])?", cell)
        if not m2: break
        g = parse_group_at(cell, m2.end())
        if not g: break
        cell = cell[:m2.start()] + g[0].replace("\\\\", " ") + cell[g[1]:]
    text = latex_to_text(cell).strip()
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
    return max(1, len(head_rows))


def parse_display(block: str) -> Display:
    is_figure = bool(re.search(r"\\includegraphics(?:\[[^]]*\])?\{", block))
    caption = extract_command(block, "caption") or extract_command(block, "caption*")
    label = extract_command(block, "label")
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
        )
    # A table note sits after the tabular in \begin{flushleft}...\end{flushleft}; the PDF
    # printed it and Word dropped it until 0.8.4 (JL 260928, MISQ official format has "Note." paragraphs).
    notes = re.findall(r"\\begin\{flushleft\}(.*?)\\end\{flushleft\}", block, re.S)
    note = " ".join(latex_to_text(mark_emphasis(n)).strip() for n in notes if latex_to_text(n).strip())
    return Display(kind="table", block=block, caption=latex_to_text(caption), label=label,
                   rows=parse_table_rows(block), note=note, spans=parse_table_spans(block),
                   header_rows=count_header_rows(block))


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


def set_font(run, name: str = FONT, size: float = 12, bold: bool | None = None, italic: bool | None = None, color: str | None = None) -> None:
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)
    rfonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def configure_document(doc: Document, *, body_size: float = 12, line_spacing: float = 2.0) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)
    for name in ("Normal", "Title", "Subtitle", "Heading 1", "Heading 2", "Heading 3", "Caption", "List Bullet", "List Number"):
        style = doc.styles[name]
        style.font.name = FONT
        style._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)
        style.font.size = Pt(10 if name == "Caption" else body_size)
        style.paragraph_format.line_spacing = 1.0 if name == "Caption" else line_spacing
        style.paragraph_format.space_before = Pt(0)
        style.paragraph_format.space_after = Pt(0)
    # python-docx's built-in Title style is dark blue with a blue rule under it; no venue asks
    # for that (the MISQ official-format Title is black, bold, no border; JL 260928 screenshot).
    title_style = doc.styles["Title"]
    title_style.font.color.rgb = RGBColor(0, 0, 0)
    title_style.font.bold = True
    title_ppr = title_style._element.get_or_add_pPr()
    for border in title_ppr.findall(qn("w:pBdr")):
        title_ppr.remove(border)
    for name, size, before in (("Heading 1", body_size, 10), ("Heading 2", body_size, 6), ("Heading 3", body_size, 4)):
        style = doc.styles[name]
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.keep_with_next = True
    # MISQ's official-format captions are bold, upright and black (caption_plain = true)
    plain_caption = bool(PROFILE_CONFIG.get("caption_plain", False))
    doc.styles["Caption"].font.italic = not plain_caption
    doc.styles["Caption"].font.color.rgb = RGBColor(0, 0, 0) if plain_caption else RGBColor(68, 68, 68)
    doc.styles["Caption"].paragraph_format.space_before = Pt(4)
    doc.styles["Caption"].paragraph_format.space_after = Pt(6)
    doc.styles["List Bullet"].paragraph_format.left_indent = Inches(0.25)
    doc.styles["List Bullet"].paragraph_format.first_line_indent = Inches(-0.15)
    if bool(PROFILE_CONFIG.get("line_numbers", False)):
        set_line_numbering(section)


def set_line_numbering(section) -> None:
    """Apply continuous Word line numbers when the selected venue requires them."""
    sect_pr = section._sectPr
    existing = sect_pr.find(qn("w:lnNumType"))
    if existing is None:
        existing = OxmlElement("w:lnNumType")
        sect_pr.append(existing)
    existing.set(qn("w:countBy"), "1")
    existing.set(qn("w:distance"), str(PROFILE_CONFIG.get("line_number_distance", 360)))
    existing.set(qn("w:restart"), "newPage" if bool(PROFILE_CONFIG.get("restart_line_numbers_each_page", False)) else "continuous")


# ── math: LaTeX → MathML (latex2mathml) → Word OMML, so equations are native Word equations ──
# 0.8.4 (JL 260928 screenshot "The equation is not in the good format"): the Word lane flattened
# $$ Y_{ijc}^{(o)} = \beta_c^{(o)} H_j + … $$ into "Y_ijc(o) = β_c(o) H_j + …" and dropped \varepsilon.
MATH_TOKEN = re.compile(r"@@MATH(\d+)@@")
MATH_STORE: list[tuple[str, bool]] = []      # inline math pulled out of body paragraphs, by token index
DISPLAY_MATH = re.compile(r"\$\$(.+?)\$\$|\\\[(.+?)\\\]|\\begin\{(equation|align)\*?\}(.+?)\\end\{\3\*?\}", re.S)
INLINE_MATH = re.compile(r"(?<![\\$])\$([^$]+?)\$(?!\$)")
_M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _xml_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _mathml_to_omml(node) -> str:
    """A small MathML → OMML writer for the constructs latex2mathml emits for paper equations."""
    tag = node.tag.split("}")[-1]
    kids = list(node)
    inner = lambda n: "".join(_mathml_to_omml(k) for k in n) if len(n) else _mathml_to_omml_leaf(n)
    if tag in ("math", "mrow", "mstyle", "semantics", "mpadded", "mphantom"):
        return "".join(_mathml_to_omml(k) for k in kids)
    if tag in ("mi", "mn", "mo", "mtext", "ms"):
        return _mathml_to_omml_leaf(node)
    if tag == "mspace":
        return '<m:r><m:t xml:space="preserve"> </m:t></m:r>'
    if tag == "msub" and len(kids) == 2:
        return f"<m:sSub><m:e>{inner(kids[0])}</m:e><m:sub>{inner(kids[1])}</m:sub></m:sSub>"
    if tag == "msup" and len(kids) == 2:
        return f"<m:sSup><m:e>{inner(kids[0])}</m:e><m:sup>{inner(kids[1])}</m:sup></m:sSup>"
    if tag == "msubsup" and len(kids) == 3:
        return (f"<m:sSubSup><m:e>{inner(kids[0])}</m:e><m:sub>{inner(kids[1])}</m:sub>"
                f"<m:sup>{inner(kids[2])}</m:sup></m:sSubSup>")
    if tag == "mfrac" and len(kids) == 2:
        return f"<m:f><m:num>{inner(kids[0])}</m:num><m:den>{inner(kids[1])}</m:den></m:f>"
    if tag in ("munder", "mover", "munderover") and kids:
        return "".join(_mathml_to_omml(k) for k in kids)
    return "".join(_mathml_to_omml(k) for k in kids) or _mathml_to_omml_leaf(node)


def _mathml_to_omml_leaf(node) -> str:
    text = (node.text or "")
    if not text:
        return ""
    variant = node.get("mathvariant", "")
    tag = node.tag.split("}")[-1]
    sty = {"bold": "b", "bold-italic": "bi", "normal": "p"}.get(variant, "p" if tag in ("mn", "mo", "mtext") else "")
    rpr = f'<m:rPr><m:sty m:val="{sty}"/></m:rPr>' if sty else ""
    return f'<m:r>{rpr}<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr><m:t xml:space="preserve">{_xml_escape(text)}</m:t></m:r>'


def latex_to_omml(latex: str):
    """An <m:oMath> element for one LaTeX math string, or None when it cannot be converted."""
    try:
        from latex2mathml.converter import convert
        from lxml import etree
        from docx.oxml import parse_xml
        mathml = etree.fromstring(convert(latex.strip()).encode("utf-8"))
        body = _mathml_to_omml(mathml)
        if not body:
            return None
        return parse_xml(f'<m:oMath xmlns:m="{_M}" xmlns:w="{_W}">{body}</m:oMath>')
    except Exception:
        return None


def protect_math(value: str, store: list[tuple[str, bool]]) -> str:
    """Swap every inline $…$ for a @@MATHn@@ token before latex_to_text flattens it."""
    def keep(match):
        store.append((match.group(1), False))
        return f"@@MATH{len(store) - 1}@@"
    return INLINE_MATH.sub(keep, value)


def add_math_paragraph(doc: Document, latex: str, *, size: float = 12) -> None:
    """A display equation, centred on its own line; plain text if it cannot be converted."""
    omath = latex_to_omml(latex)
    if omath is None:
        add_text(doc, latex_to_text("$" + latex + "$"), size=size, align=WD_ALIGN_PARAGRAPH.CENTER)
        return
    from docx.oxml import parse_xml
    paragraph = doc.add_paragraph(style="Normal")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.line_spacing = 1.5
    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(6)
    para = parse_xml(f'<m:oMathPara xmlns:m="{_M}"/>')
    para.append(omath)
    paragraph._p.append(para)


# \textbf / \textit / \emph survive latex_to_text as these marker characters (neither word
# characters nor whitespace), so add_rich_text prints them bold or italic (0.8.4, JL 260928
# appendix screenshot: "Agreeableness specification" lost its bold; 11 \textit were plain).
EMPHASIS_MARKS = {"textbf": ("\x02", "\x03"), "textit": ("\x04", "\x05"), "emph": ("\x04", "\x05")}
EMPHASIS_SWITCH = {"\x02": ("bold", True), "\x03": ("bold", False), "\x04": ("italic", True), "\x05": ("italic", False)}
RICH_PART = re.compile(r"(@@MATH\d+@@|[\x02-\x05])")


def mark_emphasis(value: str) -> str:
    pattern = re.compile(r"\\(textbf|textit|emph)\s*(?=\{)")
    while (match := pattern.search(value)) is not None:
        group = parse_group_at(value, match.end())
        if group is None:
            return value
        inner, end = group
        on, off = EMPHASIS_MARKS[match.group(1)]
        value = value[:match.start()] + on + inner + off + value[end:]
    return value


def add_rich_text(doc: Document, text: str, maths: list[tuple[str, bool]], *, size: float = 12,
                  line_spacing: float = 2.0, before: float = 0, after: float = 0) -> None:
    """A body paragraph whose @@MATHn@@ tokens become inline Word equations and whose
    emphasis marks become bold or italic runs."""
    if not RICH_PART.search(text):
        add_text(doc, text, size=size, line_spacing=line_spacing, before=before, after=after)
        return
    paragraph = doc.add_paragraph(style="Normal")
    paragraph.paragraph_format.line_spacing = line_spacing
    paragraph.paragraph_format.space_before = Pt(before)
    paragraph.paragraph_format.space_after = Pt(after)
    state = {"bold": False, "italic": False}
    for part in RICH_PART.split(text):
        if not part:
            continue
        if part in EMPHASIS_SWITCH:
            key, on = EMPHASIS_SWITCH[part]
            state[key] = on
        elif (match := MATH_TOKEN.fullmatch(part)) is not None:
            latex = maths[int(match.group(1))][0] if int(match.group(1)) < len(maths) else ""
            omath = latex_to_omml(latex)
            if omath is None:
                set_font(paragraph.add_run(latex_to_text("$" + latex + "$")), size=size)
            else:
                paragraph._p.append(omath)
        else:
            set_font(paragraph.add_run(part), size=size,
                     bold=True if state["bold"] else None, italic=True if state["italic"] else None)


def add_text(doc: Document, text: str, *, size: float = 12, bold: bool = False, align=None, style: str = "Normal",
             line_spacing: float = 2.0, before: float = 0, after: float = 0) -> None:
    if not text:
        return
    paragraph = doc.add_paragraph(style=style)
    paragraph.alignment = align
    paragraph.paragraph_format.line_spacing = line_spacing
    paragraph.paragraph_format.space_before = Pt(before)
    paragraph.paragraph_format.space_after = Pt(after)
    run = paragraph.add_run(text)
    action = "[AUTHOR ACTION REQUIRED" in text or "[TODO:" in text or "[not independently verified]" in text
    set_font(run, size=size, bold=bold, color="C00000" if action else None)


def add_heading(doc: Document, text: str, level: int = 1, *, upper: bool = True) -> None:
    if not text:
        return
    heading_style = str(PROFILE_CONFIG.get("heading_style", "heading")).lower()
    style = "Normal" if heading_style == "normal" else f"Heading {min(level, 3)}"
    paragraph = doc.add_paragraph(style=style)
    if str(PROFILE_CONFIG.get("heading_align", "left")).lower() == "center":   # MISQ centres its headings
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.keep_with_next = bool(PROFILE_CONFIG.get("headings_keep_with_next", True))
    paragraph.paragraph_format.line_spacing = 2.0
    # An explicit before-space keeps LibreOffice's DOCX renderer from visually
    # joining an immediately preceding body paragraph and its next heading.
    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(0)
    run = paragraph.add_run(text.upper() if (level == 1 and upper) else text)
    set_font(run, size=12, bold=True)


def add_bullet(doc: Document, text: str) -> None:
    paragraph = doc.add_paragraph(style="List Bullet")
    paragraph.paragraph_format.line_spacing = 2.0
    run = paragraph.add_run(text)
    set_font(run, size=12)


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top: int = 80, start: int = 120, bottom: int = 80, end: int = 120) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for name, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{name}"))
        if node is None:
            node = OxmlElement(f"w:{name}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_geometry(table, widths: list[int], *, margin: int = 120) -> None:
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    total = sum(widths)
    tbl_pr = table._tbl.tblPr
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.insert(0, tbl_w)
    tbl_w.set(qn("w:w"), str(total))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), "120")
    tbl_ind.set(qn("w:type"), "dxa")
    layout = tbl_pr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)
    for row in table.rows:
        for index, cell in enumerate(row.cells):
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.find(qn("w:tcW"))
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:w"), str(widths[min(index, len(widths) - 1)]))
            tc_w.set(qn("w:type"), "dxa")
            set_cell_margins(cell, top=80 if margin >= 120 else 40, start=margin, bottom=80 if margin >= 120 else 40, end=margin)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def cant_split(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:cantSplit")) is None:
        tr_pr.append(OxmlElement("w:cantSplit"))


def mark_header_row(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    tr_pr.append(header)


def add_table(doc: Document, display: Display, title: str = "", *, compact: bool = False) -> None:
    rows = display.rows or []
    if title or display.caption:
        caption = f"{title}. " if title else ""
        caption += display.caption
        add_text(doc, caption.strip(), size=10 if compact else 11, bold=True, style="Caption")
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
    if str(PROFILE_CONFIG.get("table_borders", "grid")).lower() == "horizontal":
        set_horizontal_borders(table)   # MISQ official format: top, bottom and row rules, no vertical lines
    header_fill = str(PROFILE_CONFIG.get("table_header_fill", "F2F4F7")).strip()
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
            run = paragraph.add_run(value)
            set_font(run, size=cell_size, bold=(row_index < heads))
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
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER


def set_horizontal_borders(table) -> None:
    """Replace the grid with horizontal rules only: top, bottom and between rows."""
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = borders.find(qn(f"w:{edge}"))
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        vertical = edge in ("left", "right", "insideV")
        element.set(qn("w:val"), "nil" if vertical else "single")
        if not vertical:
            element.set(qn("w:sz"), "4")
            element.set(qn("w:space"), "0")
            element.set(qn("w:color"), "000000")


CODE_FONT = "Courier New"
CODE_BOX_MARK = "verbatim"


def add_code_block(doc: Document, body: str, *, size: float = 9) -> None:
    """A verbatim block (a published prompt) as a framed one-cell box: one paragraph per
    source line, typewriter font, single-spaced, indentation kept, and a long line wraps
    with a two-character hanging indent, as fvextra's breaklines does in the PDF (0.8.4)."""
    lines = body.expandtabs(4).strip("\n").split("\n")
    table = doc.add_table(rows=1, cols=1)
    set_table_geometry(table, [9360], margin=120)
    table._tbl.tblPr.find(qn("w:tblInd")).set(qn("w:w"), "0")
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right"):
        element = OxmlElement(f"w:{edge}")
        for key, val in (("val", "single"), ("sz", "4"), ("space", "0"), ("color", "000000")):
            element.set(qn(f"w:{key}"), val)
        borders.append(element)
    tbl_pr = table._tbl.tblPr
    old = tbl_pr.find(qn("w:tblBorders"))
    if old is not None:
        tbl_pr.remove(old)
    later = next((c for c in tbl_pr if c.tag in {qn("w:shd"), qn("w:tblLayout"), qn("w:tblCellMar"), qn("w:tblLook")}), None)
    if later is not None:
        later.addprevious(borders)          # CT_TblPr order: tblBorders before shd/tblLayout/tblCellMar/tblLook
    else:
        tbl_pr.append(borders)
    marker = OxmlElement("w:tblDescription")   # last in CT_TblPr; docx_table_count skips these boxes
    marker.set(qn("w:val"), CODE_BOX_MARK)
    tbl_pr.append(marker)
    cell = table.cell(0, 0)
    char = size * 20 * 0.6                      # Courier advances 0.6 em per character, in twips
    for index, line in enumerate(lines):
        paragraph = cell.paragraphs[0] if index == 0 else cell.add_paragraph()
        text = line.rstrip()
        lead = len(text) - len(text.lstrip(" "))
        fmt = paragraph.paragraph_format
        fmt.space_before = fmt.space_after = Pt(0)
        fmt.line_spacing = 1.0
        fmt.left_indent = Pt((lead + 2) * char / 20)
        fmt.first_line_indent = Pt(-2 * char / 20)
        run = paragraph.add_run(text.lstrip(" ") or " ")
        set_font(run, CODE_FONT, size=size)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(6)
    spacer.paragraph_format.line_spacing = 1.0


def ensure_asset(display: Display, name: str) -> Path | None:
    if display.image_path is None:
        return None
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    target = ASSET_DIR / name
    source = display.image_path
    if source.suffix.lower() == ".pdf":
        subprocess.run(
            ["pdftoppm", "-png", "-singlefile", "-r", "180", str(source), str(target.with_suffix(""))],
            check=True,
        )
        return target
    shutil.copy2(source, target)
    return target


def add_figure(doc: Document, display: Display, title: str = "", *, compact: bool = False) -> None:
    base_name = title or Path(display.image_ref).stem or "figure"
    filename = re.sub(r"[^A-Za-z0-9._-]+", "-", base_name).strip("-") + ".png"
    image = ensure_asset(display, filename)
    if image is None:
        add_text(doc, f"{title}: image source not found.", size=10 if compact else 11)
        return
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.keep_with_next = True
    run = paragraph.add_run()
    shape = run.add_picture(str(image), width=Inches(6.1))
    alt = display.caption or title or display.image_ref
    shape._inline.docPr.set("descr", alt[:500])
    shape._inline.docPr.set("title", filename)
    caption = f"{title}. " if title else ""
    caption += display.caption
    add_text(doc, caption.strip(), size=10 if compact else 11, style="Caption")


def add_events(doc: Document, events: Iterable[Event], *, include_displays: bool = True, compact: bool = False,
               number_displays: bool = False, main_numbering: bool = False, appendix_letters: bool = False) -> None:
    """0.7.1: ``number_displays`` gives every table/figure in this stream a running
    title ("Table S1.", "Figure S1."; prefixes from the profile), so a supplement
    table no longer prints its caption with no number."""
    counters = {"table": 0, "figure": 0}
    prefixes = {"table": str(PROFILE_CONFIG.get("supplement_table_prefix", "Table S")),
                "figure": str(PROFILE_CONFIG.get("supplement_figure_prefix", "Figure S"))}
    if main_numbering:
        prefixes = {"table": str(PROFILE_CONFIG.get("main_table_prefix", "Table ")),
                    "figure": str(PROFILE_CONFIG.get("main_figure_prefix", "Figure "))}
    letter = 0
    for event in events:
        if event.kind == "heading":
            title = str(event.value)
            if appendix_letters and event.level == 1:
                # LaTeX's \appendix letters its sections; Word printed the bare title in
                # caps, so "Appendix A." was nowhere in the .docx while the LaTeX PDF and
                # the co-author's official-format file both carry it (JL 260908).
                title = f"{PROFILE_CONFIG.get('appendix_word', 'Appendix')} {chr(ord('A') + letter)}. {title}"
                if per_appendix_numbering():   # 0.8.2: Table B1 … restarts under each appendix letter
                    counters = {"table": 0, "figure": 0}
                    prefixes = {"table": f"{PROFILE_CONFIG.get('main_table_prefix', 'Table ')}{chr(ord('A') + letter)}",
                                "figure": f"{PROFILE_CONFIG.get('main_figure_prefix', 'Figure ')}{chr(ord('A') + letter)}"}
                letter += 1
            add_heading(doc, title, event.level, upper=not (appendix_letters and event.level == 1))
        elif event.kind == "text":
            add_rich_text(doc, str(event.value), MATH_STORE, size=11 if compact else 12)
        elif event.kind == "math":
            add_math_paragraph(doc, str(event.value), size=11 if compact else 12)
        elif event.kind == "code":
            add_code_block(doc, str(event.value))
        elif event.kind == "list":
            for item in event.value:  # type: ignore[union-attr]
                add_bullet(doc, str(item))
        elif event.kind == "display" and include_displays:
            display = event.value
            if isinstance(display, Display):
                title = ""
                if number_displays:
                    counters[display.kind] += 1
                    title = f"{prefixes[display.kind]}{counters[display.kind]}"
                if display.kind == "table":
                    add_table(doc, display, title, compact=compact)
                else:
                    add_figure(doc, display, title, compact=compact)


def add_abstract(doc: Document, block: str) -> None:
    add_heading(doc, str(PROFILE_CONFIG.get("abstract_heading", "ABSTRACT")), 1)
    labels = list(re.finditer(r"\\noindent\s*\\textbf\s*\{([^{}]+)\}", block))
    if not labels:
        add_text(doc, latex_to_text(block))
        return
    # Unlabelled prose before the first label (an MISQ abstract, then "Keywords:")
    # is the abstract itself; before 0.8.4 it was dropped and only the Keywords printed.
    lead = block[:labels[0].start()]
    spacing = float(PROFILE_CONFIG.get("abstract_line_spacing", 2.0))   # MISQ: single-spaced abstract and keywords
    if latex_to_text(lead).strip():
        add_text(doc, latex_to_text(lead), line_spacing=spacing)
    for index, match in enumerate(labels):
        end = labels[index + 1].start() if index + 1 < len(labels) else len(block)
        paragraph = doc.add_paragraph(style="Normal")
        paragraph.paragraph_format.line_spacing = spacing
        paragraph.paragraph_format.space_before = Pt(8 if spacing < 2 else 0)
        paragraph.paragraph_format.space_after = Pt(0)
        label_run = paragraph.add_run(latex_to_text(match.group(1)) + " ")
        body_run = paragraph.add_run(latex_to_text(block[match.end():end]))
        set_font(label_run, size=12, bold=True)
        set_font(body_run, size=12)


def extract_highlights(body: str) -> list[str]:
    heading = re.escape(str(PROFILE_CONFIG.get("highlights_heading", "Article Highlights")))
    match = re.search(rf"\\textbf\{{{heading}\}}.*?\\begin\{{itemize\}}(.*?)\\end\{{itemize\}}", body, re.S)
    if match is None:
        return []
    return list_items(match.group(0))


def add_title_page(doc: Document, title: str, running_title: str, word_count: int, table_count: int, figure_count: int, author: str) -> None:
    """The manuscript title page, as the VENUE declares it.

    This used to hard-code the medical-journal page (running title, article type,
    main-text word count, display count) for every profile whose layout was
    "generic", so the MISQ build shipped a JAMA title page: a "Running title:"
    line with no value under a profile that declares running_head = false, plus
    two build counts inside the deliverable (JL 260908: a delivered PDF or Word
    carries no process text). Fields are now named and ordered by the profile;
    the default list is the old medical set, so every existing profile is
    unchanged.
    """
    known = {
        "title":       lambda: (add_text(doc, title, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                                         style="Title", line_spacing=1.0, before=48, after=36)
                            if _front_matter_on_one_page() else
                            add_text(doc, title, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)),
        "running":     lambda: add_text(doc, f"Running title: {running_title}", align=WD_ALIGN_PARAGRAPH.CENTER),
        "author":      lambda: add_text(doc, author or str(PROFILE_CONFIG.get(
                           "author_placeholder", "[AUTHOR NAMES: first, middle, and last names]")),
                           align=WD_ALIGN_PARAGRAPH.CENTER),
        "affiliations": lambda: add_text(doc, str(PROFILE_CONFIG.get(
                           "affiliations_placeholder", "[AFFILIATIONS]")), align=WD_ALIGN_PARAGRAPH.CENTER),
        "corresponding": lambda: add_text(doc, str(PROFILE_CONFIG.get(
                           "corresponding_author_placeholder", "Corresponding author: [FULL NAME]; [email]")),
                           align=WD_ALIGN_PARAGRAPH.CENTER),
        "article_type": lambda: add_text(doc, f"Article type: {PROFILE_CONFIG.get('article_type', 'Research Article')}",
                           align=WD_ALIGN_PARAGRAPH.CENTER),
        "word_count":  lambda: add_text(doc, "Main-text word count (excluding tables, legends, title page, "
                           f"acknowledgments, and references): {word_count}", align=WD_ALIGN_PARAGRAPH.CENTER),
        "display_count": lambda: add_text(doc, f"Number of main displays: {table_count + figure_count} "
                           f"({table_count} tables, {figure_count} figures)", align=WD_ALIGN_PARAGRAPH.CENTER),
        "keywords_hint": lambda: None,
    }
    fields = PROFILE_CONFIG.get("title_page_fields", ["title", "running", "author", "affiliations",
                                                     "corresponding", "article_type", "word_count", "display_count"])
    if not isinstance(fields, list):
        fields = ["title"]
    unknown = [f for f in fields if f not in known]
    if unknown:
        raise RuntimeError("profile title_page_fields names no such field: %s (have %s)"
                           % (", ".join(unknown), ", ".join(sorted(known))))
    for field in fields:
        known[field]()
    action_fields = PROFILE_CONFIG.get("title_page_action_fields", [])
    if not isinstance(action_fields, list):
        action_fields = []
    for field in action_fields:
        add_text(doc, str(field), align=WD_ALIGN_PARAGRAPH.CENTER)
    if not _front_matter_on_one_page():   # MISQ: the abstract shares page 1; the break comes after it
        doc.add_page_break()


def _front_matter_on_one_page() -> bool:
    """profile front_matter = "title-abstract-keywords": title, abstract and keywords on page 1,
    then a page break before the first section (the MISQ official-format file, JL 260928)."""
    return str(PROFILE_CONFIG.get("front_matter", "title-page")).lower() == "title-abstract-keywords"


def labelled_blocks(doc: Document, heading: str, block: str) -> None:
    """Render JAMA Key Points or a structured abstract from labelled TeX prose."""
    add_heading(doc, heading, 1)
    labels = list(re.finditer(r"\\noindent\s*\\textbf\s*\{([^{}]+)\}", block))
    if not labels:
        add_text(doc, latex_to_text(block))
        return
    for index, match in enumerate(labels):
        end = labels[index + 1].start() if index + 1 < len(labels) else len(block)
        paragraph = doc.add_paragraph(style="Normal")
        paragraph.paragraph_format.line_spacing = 2.0
        paragraph.paragraph_format.space_after = Pt(0)
        label_run = paragraph.add_run(latex_to_text(match.group(1)) + " ")
        body_run = paragraph.add_run(latex_to_text(block[match.end():end]))
        set_font(label_run, size=12, bold=True)
        set_font(body_run, size=12)


def extract_jama_title(center_block: str) -> tuple[str, str]:
    """Read the title and blinded-author line from JAMA's source-owned title block."""
    title_part = center_block.split(r"\vspace", 1)[0]
    title_part = re.sub(r"\\(?:begin|end)\{center\}", "", title_part)
    title_part = re.sub(r"\\(?:Large|large|bfseries)\b", "", title_part)
    title = latex_to_text(title_part.replace(r"\\", " "))
    author_match = re.search(r"\vspace\{[^}]+\}\s*(.*?)\s*\vspace", center_block, re.S)
    author = latex_to_text(author_match.group(1).strip()) if author_match else ""
    return title, author


def jama_parts(raw_master: str) -> tuple[str, str, str, str, str, str]:
    """Split a JAMA IM desk room without requiring a generic abstract environment."""
    body = clean_fragment(raw_master, MASTER.parent, remove_abstract=False)
    body = body.split(r"\begin{document}", 1)[-1].split(r"\end{document}", 1)[0]
    center_match = CENTER_PATTERN.search(body)
    if center_match is None:
        raise RuntimeError("JAMA IM source is missing its title-page center block")
    title, author = extract_jama_title(center_match.group(0))

    key_match = re.search(r"\\section\*\{Key Points\}(.*?)\\section\*\{Abstract\}", body, re.S)
    abstract_match = re.search(r"\\section\*\{Abstract\}(.*?)\\section\s*\{Introduction\}", body, re.S)
    bib_match = re.search(r"\\bibliography\s*\{", body)
    appendix_match = re.search(r"\\appendix\b", body)
    if abstract_match is None or bib_match is None or appendix_match is None:
        raise RuntimeError("JAMA IM source is missing Key Points, Abstract, bibliography, or appendix boundary")
    key_points = key_match.group(1) if key_match else ""
    abstract = abstract_match.group(1)
    intro = re.search(r"\\section\s*\{Introduction\}", body)
    if intro is None:
        raise RuntimeError("JAMA IM source is missing Introduction")
    main_text = body[intro.start():bib_match.start()]
    supplement_text = body[appendix_match.end():]
    return title, author, key_points, abstract, main_text, supplement_text


def add_jama_title_page(doc: Document, title: str, author: str, main_words: int,
                        table_count: int, figure_count: int, evidence: dict[str, object]) -> None:
    """Venue-only title packaging; all study-specific text remains in the room source."""
    add_text(doc, title, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    if str(evidence.get("mode", "draft")) not in {"final", "submission", "submission-ready"}:
        add_text(doc, str(PROFILE_CONFIG.get("draft_label", "DRAFT — NOT SUBMISSION READY")),
                 align=WD_ALIGN_PARAGRAPH.CENTER)
    if author:
        add_text(doc, author, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(doc, str(PROFILE_CONFIG.get("venue_label", "JAMA Internal Medicine")),
             align=WD_ALIGN_PARAGRAPH.CENTER)
    date = str(PROFILE_CONFIG.get("document_date", "")).strip()
    if date:
        add_text(doc, date, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(doc, f"Main-text source word count: {main_words}", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(doc, f"Main displays: {table_count} tables; {figure_count} figures", align=WD_ALIGN_PARAGRAPH.CENTER)
    if evidence.get("pending_markers"):
        add_text(doc, "Evidence placeholders remain; this build is not submission-ready.",
                 align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()


def initials(author: str) -> str:
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", author)
    return "".join(token[0].upper() for token in tokens if token)


def format_authors(author_field: str) -> str:
    clean = latex_to_text(author_field)
    if not clean:
        return ""
    output: list[str] = []
    for author in re.split(r"\s+and\s+", clean):
        author = author.strip().rstrip(".")
        if author.lower() == "others":
            continue
        if "," in author:
            surname, given = [part.strip() for part in author.split(",", 1)]
            output.append(f"{surname} {initials(given)}".strip())
        else:
            parts = author.split()
            output.append(f"{parts[-1]} {initials(' '.join(parts[:-1]))}".strip() if len(parts) > 1 else author)
    if len(output) > 6:
        return ", ".join(output[:6]) + ", et al"
    return ", ".join(output)


def format_reference(key: str) -> str:
    fields = BIB[key]
    authors = format_authors(fields.get("author", ""))
    title = latex_to_text(fields.get("title", ""))
    journal = latex_to_text(fields.get("journal", fields.get("booktitle", "")))
    year = latex_to_text(fields.get("year", ""))
    volume = latex_to_text(fields.get("volume", ""))
    pages = latex_to_text(fields.get("pages", ""))
    doi = latex_to_text(fields.get("doi", ""))
    pieces = [part for part in (authors, title, journal) if part]
    tail = " ".join(part for part in (year, volume, pages) if part)
    if tail:
        pieces.append(tail)
    if doi:
        pieces.append("doi:" + doi)
    return ". ".join(pieces).rstrip(".") + "."


def apa_authors(author_field: str) -> str:
    """Barnett, M. L., Olenski, A. R., & Jena, A. B."""
    people = [a.strip().rstrip(".") for a in re.split(r"\s+and\s+", latex_to_text(author_field or "").strip())
              if a.strip() and a.strip().lower() != "others"]
    out = []
    for person in people:
        if "," in person:
            surname, given = [p.strip() for p in person.split(",", 1)]
        else:
            parts = person.split()
            surname, given = (parts[-1], " ".join(parts[:-1])) if len(parts) > 1 else (person, "")
        given = " ".join(f"{g[0]}." for g in given.split() if g)
        out.append(f"{surname}, {given}".strip().rstrip(","))
    if not out:
        return ""
    if len(out) == 1:
        return out[0]
    return ", ".join(out[:-1]) + ", & " + out[-1]


def format_reference_apa(key: str) -> str:
    f = BIB[key]
    bits = [apa_authors(f.get("author", "")), f"({latex_to_text(f.get('year', 'n.d.'))})."]
    title = latex_to_text(f.get("title", "")).rstrip(".")
    if title:
        bits.append(title + ".")
    journal = latex_to_text(f.get("journal", f.get("booktitle", ""))).rstrip(".")
    volume = latex_to_text(f.get("volume", ""))
    pages = latex_to_text(f.get("pages", "")).replace("--", "-")
    if journal:
        tail = journal + (f", {volume}" if volume else "") + (f", {pages}" if pages else "")
        bits.append(tail + ".")
    doi = latex_to_text(f.get("doi", "")).strip()
    if doi:
        bits.append("https://doi.org/" + doi)
    return " ".join(b for b in bits if b).replace("..", ".")


def add_references(doc: Document) -> None:
    if not CITATION_NUMBERS:
        return
    add_heading(doc, str(PROFILE_CONFIG.get("references_heading", "REFERENCES")), 1)
    if author_date_style():
        # alphabetical by first author, no numbers: the order a reader looks a name up in
        for key in sorted(CITATION_NUMBERS, key=lambda k: (surname_of(BIB[k].get("author", "")).lower(),
                                                           latex_to_text(BIB[k].get("year", "")))):
            paragraph = doc.add_paragraph(style="Normal")
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.left_indent = Inches(0.5)
            paragraph.paragraph_format.first_line_indent = Inches(-0.5)
            set_font(paragraph.add_run(format_reference_apa(key)), size=11)
        return
    for number, key in enumerate(CITATION_NUMBERS, start=1):
        paragraph = doc.add_paragraph(style="Normal")
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.line_spacing = 1.0
        paragraph.paragraph_format.left_indent = Inches(0.25)
        paragraph.paragraph_format.first_line_indent = Inches(-0.25)
        run = paragraph.add_run(f"{number}. {format_reference(key)}")
        set_font(run, size=11)


def clean_fragment(raw: str, base: Path, *, remove_abstract: bool = True) -> str:
    value = expand_inputs(raw, base)
    value = strip_comments(value)
    if remove_abstract:
        value = re.sub(r"\\(?:begin|end)\{abstract\}", "", value)
    return value


def word_count(events: Iterable[Event]) -> int:
    words = []
    for event in events:
        if event.kind in {"text", "list"}:
            values = event.value if event.kind == "list" else [event.value]
            words.extend(re.findall(r"\b[\w%]+(?:[–-][\w%]+)?\b",
                                    MATH_TOKEN.sub(" ", " ".join(str(v) for v in values))))
    return len(words)


def write_section_snapshots(section_specs: list[tuple[str, str]], running_title: str) -> None:
    DRAFT_SECTION_ROOM.mkdir(parents=True, exist_ok=True)
    readme = DRAFT_SECTION_ROOM / "README.md"
    readme.write_text(
        "# Generated section snapshots\n\n"
        "These DOCX files are generated from the configured desk-room sections by the shared "
        "`haipipe-paper-assemble` engine, launched through this paper's thin wrapper. "
        "They are review snapshots only and are never used as builder inputs.\n",
        encoding="utf-8",
    )
    written = set()
    for source_name, label in section_specs:
        source = SECTION_DIR / source_name
        text = clean_fragment(source.read_text(encoding="utf-8"), source.parent)
        events, _ = parse_events(text)
        doc = Document()
        configure_document(doc)
        add_title_page(doc, label, running_title, word_count(events), 0, 0, "Authors hidden for review")
        add_events(doc, events, include_displays=True)
        output_name = source_name.replace("_", "-").replace(".tex", ".docx")
        doc.save(DRAFT_SECTION_ROOM / output_name)
        written.add(output_name)
    # the folder is regenerated whole: a snapshot no section makes any more (a renamed Section's old name) goes
    for stale in DRAFT_SECTION_ROOM.glob("*.docx"):
        if stale.name not in written:
            stale.unlink()


def evidence_lock_path() -> Path | None:
    """Return the materialized room-local evidence receipt, when configured."""
    raw = EVIDENCE_CONFIG.get("lock")
    if not raw:
        return None
    path = Path(str(raw))
    return path if path.is_absolute() else (WORD_ROOM / path).resolve()


def evidence_preflight() -> dict[str, object]:
    """Validate evidence state without creating or replacing manuscript prose.

    The Section projection owns the words.  The lock records which Page Evidence
    Items those words depend on.  A draft can keep visible ``[E## pending]``
    markers; a final build cannot.
    """
    mode = str(EVIDENCE_CONFIG.get("mode", "none")).lower()
    path = evidence_lock_path()
    source_text = "\n".join(path.read_text(encoding="utf-8", errors="replace")
                            for path in sorted(SECTION_DIR.glob("*.tex")))
    pending_markers = sorted(set(re.findall(r"\[E\d{2}\s+pending\]", source_text)))
    report: dict[str, object] = {
        "mode": mode,
        "lock": str(path.relative_to(ROOT)) if path and path.is_relative_to(ROOT) else (str(path) if path else None),
        "pending_markers": pending_markers,
        "items": 0,
        "unaccepted_items": [],
        "lock_exists": path.exists() if path else None,
    }
    if path is None:
        return report
    if not path.exists():
        raise FileNotFoundError(f"Configured evidence lock not found: {path}")
    lock = json.loads(path.read_text(encoding="utf-8"))
    items = lock.get("items", [])
    if not isinstance(items, list):
        raise ValueError(f"Evidence lock has non-list items: {path}")
    unaccepted = [
        f"{item.get('page', 'unknown')}/{item.get('item', 'unknown')} ({item.get('state', 'unknown')})"
        for item in items if isinstance(item, dict) and item.get("state") != "accepted"
    ]
    report["items"] = len(items)
    report["unaccepted_items"] = unaccepted
    if mode in {"final", "submission", "submission-ready"} and (pending_markers or unaccepted):
        raise RuntimeError(
            "Final build blocked by unresolved evidence: "
            + ", ".join(pending_markers + unaccepted)
        )
    return report


def source_manifest() -> dict[str, object]:
    paths = [MASTER, BIB_PATH]
    paths.extend(sorted(SECTION_DIR.glob("*.tex")))
    paths.extend(sorted(DISPLAY_DIR.rglob("*.tex")))
    paths.extend(sorted(DISPLAY_DIR.rglob("*.png")))
    paths.extend(sorted(DISPLAY_DIR.rglob("*.pdf")))
    lock_path = evidence_lock_path()
    if lock_path and lock_path.exists():
        paths.append(lock_path)
    # 0.8.4 (JL 260928 "Why we have the sha256? remove that, waste my tokens"): the manifest lists
    # its inputs by path only; nothing ever read the 74 hashes it used to carry.
    files = [str(path.relative_to(ROOT)) for path in paths]
    profile_path = PROFILE_ROOT / f"{PROFILE_NAME}.toml" if PROFILE_NAME else None
    return {
        "engine": "haipipe-paper-assemble/latex_room_to_docx-0.2.1",
        "builder": "haipipe-paper-assemble/scripts/latex_room_to_docx.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)) if CONFIG_PATH.exists() else None,
        "profile": str(profile_path.relative_to(SKILL_ROOT)) if profile_path and profile_path.exists() else None,
        "venue_profile": PROFILE_CONFIG.get("venue_profile", BUILD_CONFIG.get("paper", {}).get("venue_profile")),
        "source_of_record": str(MASTER.relative_to(ROOT)),
        "outputs": [
            str(MAIN_PATH.relative_to(ROOT)),
            str(SUPP_PATH.relative_to(ROOT)),
            str(MAIN_PDF_PATH.relative_to(ROOT)),
            str(SUPP_PDF_PATH.relative_to(ROOT)),
            str(DRAFT_SECTION_ROOM.relative_to(ROOT)),
            str(MANIFEST_PATH.relative_to(ROOT)),
        ],
        "files": files,
    }


def render_submission_pdfs() -> dict[str, object]:
    """Render configured DOCX deliverables to PDFs when LibreOffice is available."""
    soffice = shutil.which("soffice")
    report: dict[str, object] = {
        "renderer": "LibreOffice" if soffice else None,
        "available": bool(soffice),
        "outputs": [],
        "errors": [],
    }
    if not soffice:
        return report
    for docx_path, pdf_path in ((MAIN_PATH, MAIN_PDF_PATH), (SUPP_PATH, SUPP_PDF_PATH)):
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(
                [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(pdf_path.parent), str(docx_path)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            produced = pdf_path.parent / docx_path.with_suffix(".pdf").name
            if produced != pdf_path and produced.exists():
                shutil.move(str(produced), str(pdf_path))
            if not pdf_path.exists():
                raise RuntimeError(f"LibreOffice did not create {pdf_path.name}")
            report["outputs"].append(str(pdf_path.relative_to(ROOT)))  # type: ignore[index]
        except (OSError, subprocess.CalledProcessError, RuntimeError) as error:
            report["errors"].append(f"{docx_path.name}: {error}")  # type: ignore[index]
    return report


def write_common_receipts(main_events: list[Event], main_displays: list[Display],
                          supplement_events: list[Event], running_title: str,
                          evidence: dict[str, object], pdf_report: dict[str, object]) -> None:
    """Write derived receipts only; they are never inputs to a later build."""
    snapshot_config = BUILD_CONFIG.get("snapshots", {})
    configured_sections = snapshot_config.get("sections", []) if isinstance(snapshot_config, dict) else []
    section_specs = [
        (str(item["source"]), str(item["label"]))
        for item in configured_sections
        if isinstance(item, dict) and "source" in item and "label" in item
    ]
    if not section_specs:
        section_specs = [
            (path.name, path.stem.replace("_", " ").title())
            for path in sorted(SECTION_DIR.glob("*.tex"))
        ]
    # 0.8.4 (JL 260928: "why it is not the same to each section's word? and no references"): the
    # snapshots are a second, reference-less copy of what each Section Page already delivers in
    # its own delivery/word/; section_snapshots = "" switches them off.
    if str(OUTPUT_CONFIG.get("section_snapshots", "draft-sections")).strip():
        write_section_snapshots(section_specs, running_title)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    manifest = source_manifest()
    manifest["evidence"] = evidence
    word_limit = PROFILE_CONFIG.get("main_text_word_limit")
    manifest["build"] = {
        "status": "DRAFT" if evidence.get("pending_markers") or evidence.get("unaccepted_items") else "CANDIDATE",
        "source_of_record": str(MASTER.relative_to(ROOT)),
        "venue_profile": PROFILE_NAME,
        "main_text_words": word_count(main_events),
        "main_text_word_limit": word_limit,
        "citations": len(CITATION_NUMBERS),
        "main_tables": len([display for display in main_displays if display.kind == "table"]),
        "main_figures": len([display for display in main_displays if display.kind == "figure"]),
        "supplement_events": len(supplement_events),
        "evidence": evidence,
        "pdf": pdf_report,
        "checks": {
            "master_exists": MASTER.exists(),
            "bibliography_exists": BIB_PATH.exists(),
            "citations_resolved": True,
            "within_declared_word_limit": (
                word_limit is None or word_count(main_events) <= int(word_limit)
            ),
            "evidence_lock_exists": evidence.get("lock_exists"),
            "no_pending_evidence": not evidence.get("pending_markers") and not evidence.get("unaccepted_items"),
            "pdf_outputs_rendered": not pdf_report.get("available") or not pdf_report.get("errors"),
            "g6_human_decision": False,
        },
    }
    manifest["render"] = pdf_report
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_jama_internal_medicine(raw_master: str, evidence: dict[str, object]) -> tuple[Path, Path]:
    """JAMA IM is a venue profile, not a paper-specific renderer."""
    title, author, key_points, abstract, main_text, supplement_text = jama_parts(raw_master)
    main_events, main_displays = parse_events(main_text)
    supplement_events, _ = parse_events(supplement_text)
    missing = [key for key in CITATION_NUMBERS if key not in BIB]
    if missing:
        raise RuntimeError(f"Citations missing from reference.bib: {missing}")
    main_tables = [display for display in main_displays if display.kind == "table"]
    main_figures = [display for display in main_displays if display.kind == "figure"]
    MAIN_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUPP_PATH.parent.mkdir(parents=True, exist_ok=True)

    main_doc = Document()
    configure_document(main_doc)
    add_jama_title_page(main_doc, title, author, word_count(main_events), len(main_tables), len(main_figures), evidence)
    if key_points:
        labelled_blocks(main_doc, str(PROFILE_CONFIG.get("key_points_heading", "KEY POINTS")), key_points)
    labelled_blocks(main_doc, str(PROFILE_CONFIG.get("abstract_heading", "ABSTRACT")), abstract)
    add_events(main_doc, main_events, include_displays=bool(PROFILE_CONFIG.get("include_main_displays", False)))
    add_references(main_doc)
    main_doc.save(MAIN_PATH)

    supp_doc = Document()
    configure_document(supp_doc, body_size=11, line_spacing=1.5)
    add_text(supp_doc, title, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(supp_doc, str(PROFILE_CONFIG.get("supplement_title", "ONLINE-ONLY SUPPLEMENTAL MATERIAL")),
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    supp_doc.add_page_break()
    add_events(supp_doc, supplement_events, include_displays=True, compact=True)
    supp_doc.save(SUPP_PATH)

    pdf_report = render_submission_pdfs()
    write_common_receipts(main_events, main_displays, supplement_events, title, evidence, pdf_report)
    return MAIN_PATH, SUPP_PATH


def build() -> tuple[Path, Path]:
    if not MASTER.exists():
        raise FileNotFoundError(MASTER)
    if not BIB_PATH.exists():
        raise FileNotFoundError(BIB_PATH)

    # submission-assets/ is a derived folder named by the CURRENT build's figures.
    # Nothing ever removed a stale name, so a figure that was renamed or dropped
    # kept shipping alongside its replacement (Figure-2.png outliving Figure 2).
    if ASSET_DIR.is_dir():
        for stale in ASSET_DIR.iterdir():
            if stale.is_file():
                stale.unlink()

    global BIB, CITATION_NUMBERS, REF_NUMBERS, REF_TEXT
    BIB = parse_bib(BIB_PATH.read_text(encoding="utf-8"))
    CITATION_NUMBERS = {}
    REF_NUMBERS = {}
    REF_TEXT = {}

    raw_master = MASTER.read_text(encoding="utf-8")
    evidence = evidence_preflight()
    if str(PROFILE_CONFIG.get("layout", "")).lower() == "jama-internal-medicine":
        return build_jama_internal_medicine(raw_master, evidence)
    running_match = re.search(r"Running title\s*\(<[^>]+>\):\s*(.+)", raw_master)
    running_title = running_match.group(1).strip() if running_match else RUNNING_TITLE_FALLBACK
    title = latex_to_text(extract_command(raw_master, "title"))
    author = latex_to_text(extract_command(raw_master, "author"))
    body = clean_fragment(raw_master, MASTER.parent, remove_abstract=False)
    body = body.split(r"\begin{document}", 1)[-1].split(r"\end{document}", 1)[0]
    register_labels(body)

    abstract_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, re.S)
    if abstract_match is None:
        raise RuntimeError("Master manuscript has no abstract environment")
    abstract = abstract_match.group(1)
    highlights = extract_highlights(body)
    backmatter_heading = str(PROFILE_CONFIG.get("backmatter_heading", "Acknowledgments"))
    ack_match = re.search(r"\\section\*?\s*\{" + re.escape(backmatter_heading) + r"\}", body)
    bib_match = re.search(r"\\bibliographystyle\s*\{", body)
    appendix_match = re.search(r"\\appendix\b", body)
    if bib_match is None or appendix_match is None:
        raise RuntimeError("Master manuscript is missing the bibliography or appendix boundary")
    # 0.8.4: a blind copy (profile [latex] acknowledgments = false) has no back-matter section;
    # the main text then runs to the bibliography.
    main_end = ack_match.start() if ack_match is not None else bib_match.start()
    main_text = body[abstract_match.end():main_end]
    back_text = body[main_end:bib_match.start()]
    supplement_text = body[appendix_match.end():]
    main_events, main_displays = parse_events(main_text)
    back_events, _ = parse_events(back_text)
    supplement_events, _ = parse_events(supplement_text)
    missing = [key for key in CITATION_NUMBERS if key not in BIB]
    if missing:
        raise RuntimeError(f"Citations missing from reference.bib: {missing}")

    main_tables = [display for display in main_displays if display.kind == "table"]
    main_figures = [display for display in main_displays if display.kind == "figure"]
    MAIN_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUPP_PATH.parent.mkdir(parents=True, exist_ok=True)

    main_doc = Document()
    configure_document(main_doc)
    add_title_page(main_doc, title, running_title, word_count(main_events), len(main_tables), len(main_figures), author)
    add_abstract(main_doc, abstract)
    if _front_matter_on_one_page():
        main_doc.add_page_break()
    # An empty heading is a defect, not a section: the MISQ build printed
    # "ARTICLE HIGHLIGHTS" with nothing under it, because the heading was
    # unconditional and only the bullets came from the body (JL 260908).
    if highlights:
        add_heading(main_doc, str(PROFILE_CONFIG.get("highlights_heading", "Article Highlights")), 1)
        for highlight in highlights:
            add_bullet(main_doc, highlight)
    inline_displays = str(PROFILE_CONFIG.get("displays_position", "end")).lower() == "inline"
    add_events(main_doc, main_events, include_displays=inline_displays,
               number_displays=inline_displays, main_numbering=True)
    add_events(main_doc, back_events, include_displays=False)
    add_references(main_doc)
    # Displays after the references is the MEDICAL convention. A venue whose
    # profile places displays inline wants them where the prose cites them, and
    # the MISQ profile already says displays = "inline" for the LaTeX lane; Word
    # printed them twice as often as it should have (JL 260908).
    if str(PROFILE_CONFIG.get("displays_position", "end")).lower() == "end":
        if main_tables:
            add_heading(main_doc, str(PROFILE_CONFIG.get("tables_heading", "TABLES")), 1)
            for number, display in enumerate(main_tables, start=1):
                add_table(main_doc, display, f"Table {number}")
        if main_figures:
            add_heading(main_doc, str(PROFILE_CONFIG.get("figures_heading", "FIGURE LEGENDS")), 1)
            for number, display in enumerate(main_figures, start=1):
                add_figure(main_doc, display, f"Figure {number}")
    # WHERE THE APPENDICES GO is the venue's call, not a constant. A separate
    # "ONLINE-ONLY SUPPLEMENTAL MATERIAL" file is the MEDICAL convention; MISQ keeps
    # Appendix A-E inside the one manuscript after the references, which is what the
    # co-author's MISQ-Official-Format.docx does (JL 260908 "is the word fit the misq
    # template as well?"). When they go in the main document the supplement is not
    # written, and a stale one from an earlier profile is deleted rather than left
    # on disk to be submitted by mistake.
    appendices_in_main = str(PROFILE_CONFIG.get("appendices", "supplement")).lower() == "main"
    if appendices_in_main:
        add_events(main_doc, supplement_events, include_displays=True, number_displays=True,
                   appendix_letters=True)
    main_doc.save(MAIN_PATH)
    if appendices_in_main:
        for stale in (SUPP_PATH, SUPP_PDF_PATH):
            if stale.exists():
                stale.unlink()
        pdf_report = render_submission_pdfs()
        write_common_receipts(main_events, main_displays, supplement_events, running_title, evidence, pdf_report)
        return MAIN_PATH, None

    supp_doc = Document()
    configure_document(supp_doc, body_size=11, line_spacing=1.5)
    add_text(supp_doc, title, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(supp_doc, str(PROFILE_CONFIG.get("supplement_title", "ONLINE-ONLY SUPPLEMENTAL MATERIAL")), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(supp_doc, "[AUTHOR ACTION REQUIRED: confirm that all supplement citations, table labels, and figure labels match the final main manuscript]", size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    supp_doc.add_page_break()
    add_events(supp_doc, supplement_events, include_displays=True, compact=True, number_displays=True,
               appendix_letters=True)
    supp_doc.save(SUPP_PATH)

    pdf_report = render_submission_pdfs()
    write_common_receipts(main_events, main_displays, supplement_events, running_title, evidence, pdf_report)
    # 0.7.1 tooth (Paper-MISQ-Board, JL 260908): every table float the master prints must
    # arrive in a Word file as a real <w:tbl>. Counted AFTER the files are written, so
    # the evidence is on disk; a mismatch is loud (non-zero exit), never a silent gap.
    supp_tables = sum(1 for e in supplement_events if e.kind == "display" and isinstance(e.value, Display) and e.value.kind == "table")
    master_tables = len([1 for m_ in DISPLAY_PATTERN.finditer(body) if m_.group(1).startswith("table")])
    report = {"main": {"expected": len(main_tables), "found": docx_table_count(MAIN_PATH)},
              "supplement": {"expected": supp_tables, "found": docx_table_count(SUPP_PATH)},
              "master_table_floats": master_tables}
    ok = (report["main"]["expected"] == report["main"]["found"]
          and report["supplement"]["expected"] == report["supplement"]["found"]
          and master_tables == len(main_tables) + supp_tables)
    report["ok"] = ok
    record_tables_rendered(report)
    if not ok:
        raise RuntimeError(f"Word tables lost: {json.dumps(report)}")
    return MAIN_PATH, SUPP_PATH


def docx_table_count(path: Path) -> int:
    """how many real tables (<w:tbl>) a .docx carries; the Word-side truth. A verbatim
    box is a one-cell table too, so it is marked and not counted (0.8.4)."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    return xml.count("<w:tbl>") - xml.count(f'<w:tblDescription w:val="{CODE_BOX_MARK}"/>')


def record_tables_rendered(report: dict) -> None:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    manifest.setdefault("build", {}).setdefault("checks", {})["tables_rendered"] = report
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    main_path, supp_path = build()
    print(f"Wrote {main_path}")
    print(f"Wrote {supp_path}")
    print(f"Wrote section snapshots to {DRAFT_SECTION_ROOM}")
    print(f"Wrote source manifest to {MANIFEST_PATH}")
    print(f"Citation count: {len(CITATION_NUMBERS)}")


if __name__ == "__main__":
    main()
