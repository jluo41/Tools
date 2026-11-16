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
import sys
from copy import deepcopy
import tomllib
from typing import Iterable

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.shared import Inches, Pt, RGBColor


def _load_part(name: str) -> None:
    """Run a part file beside this engine (latex_parse.py, venue_jama.py, docx_receipts.py) inside this module's
    namespace, so its functions read this paper's config and stay reachable as latex_room_to_docx.<name>."""
    path = Path(__file__).resolve().with_name(name)
    doc = globals().get("__doc__")
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), globals())
    globals()["__doc__"] = doc   # the part's own docstring never replaces this engine's


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
# 0.9.1: a paper that prints its supplement separately (profile appendices = "supplement") has a
# master.tex without the appendices; the engine's combined.tex holds both halves, so Word reads it
if (LATEX_ROOM / "combined.tex").is_file():
    MASTER = LATEX_ROOM / "combined.tex"
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
# body text size and line spacing (JL 261112, a 2-page grant LOI at 11 pt single-spaced); a manuscript keeps 12 pt, double
BODY_SIZE = float(PROFILE_CONFIG.get("body_size", 12))
BODY_SPACING = float(PROFILE_CONFIG.get("body_line_spacing", 2.0))
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
    heading: str = ""                      # the caption's bold title (\textbf{...}); the rest is the legend (0.12.0)


@dataclass
class Event:
    kind: str
    value: str | list[str] | Display
    level: int = 0


_load_part("latex_parse.py")   # parse_group_at ... parse_bib, latex_to_text, parse_table_rows, parse_display, parse_events


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


def word_template_path() -> Path | None:
    """0.16.0 (JL 261104: "we should have the MISQ official word template, why don't we use that one?"): the venue's own
    .docx, named by [profile] word_template, relative to paper-build.toml. The manuscript is written inside that file."""
    name = PROFILE_CONFIG.get("word_template")
    if not name:
        return None
    path = (Path(CONFIG_ENV or "paper-build.toml").resolve().parent / str(name)).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"[profile] word_template not found: {path}")
    return path


def new_main_document() -> Document:
    """The venue's template with its sample text taken out: its styles, numbering, page setup and footer stay as they
    are. With no template, a blank document set up from the profile, as before."""
    path = word_template_path()
    if path is None:
        doc = Document()
        configure_document(doc)
        return doc
    doc = Document(str(path))
    body = doc.element.body
    for element in list(body):
        if element.tag != qn("w:sectPr"):
            body.remove(element)
    props = doc.core_properties   # a blind copy carries no name, and none of the template's own
    props.author = props.last_modified_by = props.title = props.subject = props.comments = props.keywords = ""
    # what the template does not define, and the tables, figures and lists need
    names = {style.name for style in doc.styles}
    if "Caption" not in names:
        caption = doc.styles.add_style("Caption", WD_STYLE_TYPE.PARAGRAPH, builtin=True)
        caption.base_style = doc.styles["Normal"]
        caption.font.size = Pt(10)
        caption.font.bold = bool(PROFILE_CONFIG.get("caption_plain", False))
        caption.paragraph_format.line_spacing = 1.0
        caption.paragraph_format.space_before = Pt(4)
        caption.paragraph_format.space_after = Pt(6)
    if "List Bullet" not in names:
        bullet = doc.styles.add_style("List Bullet", WD_STYLE_TYPE.PARAGRAPH, builtin=True)
        bullet.base_style = doc.styles["Normal"]
        bullet.paragraph_format.left_indent = Inches(0.25)
        bullet.paragraph_format.first_line_indent = Inches(-0.15)
    return doc


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
    inner = lambda n: _mathml_children(list(n)) if len(n) else _mathml_to_omml_leaf(n)
    if tag in ("math", "mrow", "mstyle", "semantics", "mpadded", "mphantom"):
        return _mathml_children(kids)
    if tag == "msqrt":      # had no case, so the root was dropped and only its contents printed (pp-LBP-JAMA 261103)
        return f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{_mathml_children(kids)}</m:e></m:rad>'
    if tag == "mroot" and len(kids) == 2:
        return f"<m:rad><m:deg>{inner(kids[1])}</m:deg><m:e>{inner(kids[0])}</m:e></m:rad>"
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


def _mathml_children(kids: list) -> str:
    """Sibling nodes in order, with a row of letters joined into one word: latex2mathml gives each letter of
    \\mathrm{score} its own <mi>, and one run per letter printed "s c o r e" (pp-LBP-JAMA 261103)."""
    out: list[str] = []
    i = 0
    while i < len(kids):
        kid = kids[i]
        if kid.tag.split("}")[-1] == "mi" and not len(kid):
            variant, text, i = kid.get("mathvariant", ""), kid.text or "", i + 1
            while i < len(kids) and kids[i].tag.split("}")[-1] == "mi" and not len(kids[i]) \
                    and kids[i].get("mathvariant", "") == variant:
                text += kids[i].text or ""
                i += 1
            out.append(_mathml_to_omml_leaf(kid, text))
        else:
            out.append(_mathml_to_omml(kid))
            i += 1
    return "".join(out)


def _mathml_to_omml_leaf(node, text: str | None = None) -> str:
    text = (node.text or "") if text is None else text
    if not text:
        return ""
    variant = node.get("mathvariant", "")
    tag = node.tag.split("}")[-1]
    sty = {"bold": "b", "bold-italic": "bi", "normal": "p"}.get(variant, "p" if tag in ("mn", "mo", "mtext") else "")
    rpr = f'<m:rPr><m:sty m:val="{sty}"/></m:rPr>' if sty else ""
    return f'<m:r>{rpr}<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr><m:t xml:space="preserve">{_xml_escape(text)}</m:t></m:r>'


def latex_to_omml(latex: str):
    """An <m:oMath> element for one LaTeX math string, or None when it cannot be converted."""
    # A two-line equation prints as one Word equation, which Word wraps itself (JL 261104: "aligned" printed as words).
    latex = re.sub(r"\\(?:begin|end)\{(?:aligned|split|gathered)\}", " ", latex)
    latex = latex.replace("\\\\", " ").replace("&", " ").replace("{}", " ")
    latex = re.sub(r"\\[Bb]igg?l?\(", "(", latex); latex = re.sub(r"\\[Bb]igg?r?\)", ")", latex)
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
# appendix screenshot: "<Trait> specification" lost its bold; 11 \textit were plain).
EMPHASIS_MARKS = {"textbf": ("\x02", "\x03"), "textit": ("\x04", "\x05"), "emph": ("\x04", "\x05")}
EMPHASIS_SWITCH = {"\x02": ("bold", True), "\x03": ("bold", False), "\x04": ("italic", True), "\x05": ("italic", False),
                   "\x0e": ("superscript", True), "\x0f": ("superscript", False),   # \x0e \x0f: an AMA citation
                   "\x10": ("superscript", True), "\x11": ("superscript", False)}   # \x10 \x11: \textsuperscript (a note's a, b)
RICH_PART = re.compile(r"(@@MATH\d+@@|[\x02-\x05\x0e-\x11])")


def mark_superscript(value: str) -> str:
    """\\textsuperscript{a} kept as marks, so Word raises it (pp-LBP-JAMA 261103: "15 yearsa", "aThe cut chosen"). Its
    own pair: an AMA citation's marks also pull the citation against the word before it, which a note's "a" must not."""
    pattern = re.compile(r"\\textsuperscript\s*(?=\{)")
    while (match := pattern.search(value)) is not None:
        group = parse_group_at(value, match.end())
        if group is None:
            return value
        value = value[:match.start()] + "\x10" + group[0] + "\x11" + value[group[1]:]
    return value


def add_marked_runs(paragraph, value: str, *, size: float, bold: bool | None = None) -> None:
    """A table cell's text: its \\textsuperscript parts raised, the rest plain."""
    for part in re.split(r"(\x10[^\x11]*\x11)", value):
        if not part:
            continue
        raised = part.startswith("\x10")
        run = paragraph.add_run(part.strip("\x10\x11") if raised else part)
        set_font(run, size=size, bold=bold)
        if raised:
            run.font.superscript = True


def mark_emphasis(value: str) -> str:
    value = mark_superscript(value)
    pattern = re.compile(r"\\(textbf|textit|emph)\s*(?=\{)")
    while (match := pattern.search(value)) is not None:
        group = parse_group_at(value, match.end())
        if group is None:
            return value
        inner, end = group
        on, off = EMPHASIS_MARKS[match.group(1)]
        value = value[:match.start()] + on + inner + off + value[end:]
    return value


def add_rich_text(doc: Document, text: str, maths: list[tuple[str, bool]], *, size: float = BODY_SIZE,
                  line_spacing: float = BODY_SPACING, before: float = 0, after: float = 0) -> None:
    """A body paragraph whose @@MATHn@@ tokens become inline Word equations and whose
    emphasis marks become bold or italic runs."""
    if not RICH_PART.search(text):
        add_text(doc, text, size=size, line_spacing=line_spacing, before=before, after=after)
        return
    text = re.sub(r"\s+\x0e", "\x0e", text)   # a superscript citation sits against its word
    text = re.sub(r"(\x0e[^\x0f]*\x0f)([.,])", r"\2\1", text)   # AMA 3.6: after a period or comma ("reviews.14,15")
    paragraph = doc.add_paragraph(style="Normal")
    paragraph.paragraph_format.line_spacing = line_spacing
    paragraph.paragraph_format.space_before = Pt(before)
    paragraph.paragraph_format.space_after = Pt(after)
    state = {"bold": False, "italic": False, "superscript": False}
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
            run = paragraph.add_run(part)
            set_font(run, size=size, bold=True if state["bold"] else None, italic=True if state["italic"] else None)
            if state["superscript"]:
                run.font.superscript = True


def add_text(doc: Document, text: str, *, size: float = BODY_SIZE, bold: bool = False, align=None, style: str = "Normal",
             line_spacing: float = BODY_SPACING, before: float = 0, after: float = 0) -> None:
    if not text:
        return
    if ("\x0e" in text or "\x10" in text) and not bold:   # a superscript: the rich writer sets it
        add_rich_text(doc, text, MATH_STORE, size=size, line_spacing=line_spacing, before=before, after=after)
        return
    text = re.sub(r"[\x0e-\x11]", "", text)
    paragraph = doc.add_paragraph(style=style)
    paragraph.alignment = align
    paragraph.paragraph_format.line_spacing = line_spacing
    paragraph.paragraph_format.space_before = Pt(before)
    paragraph.paragraph_format.space_after = Pt(after)
    run = paragraph.add_run(text)
    action = "[AUTHOR ACTION REQUIRED" in text or "[TODO:" in text or "[not independently verified]" in text
    set_font(run, size=size, bold=bold, color="C00000" if action else None)


def add_heading(doc: Document, text: str, level: int = 1, *, upper: bool = True, unnumbered: bool = False) -> None:
    if not text:
        return
    heading_style = str(PROFILE_CONFIG.get("heading_style", "heading")).lower()
    style = "Normal" if heading_style == "normal" else f"Heading {min(level, 3)}"
    template = word_template_path() is not None
    # a template's Heading styles draw their own numbers; what is not numbered there takes its Subtitle (MISQ: Abstract, REFERENCES, APPENDIX)
    if template and unnumbered and level == 1:
        style = "Subtitle"
    paragraph = doc.add_paragraph(style=style)
    if template and unnumbered and level > 1:
        paragraph._p.get_or_add_pPr().get_or_add_numPr().get_or_add_numId().val = 0
    if str(PROFILE_CONFIG.get("heading_align", "left")).lower() == "center":   # MISQ centres its headings
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.keep_with_next = bool(PROFILE_CONFIG.get("headings_keep_with_next", True))
    paragraph.paragraph_format.line_spacing = BODY_SPACING
    # An explicit before-space keeps LibreOffice's DOCX renderer from visually
    # joining an immediately preceding body paragraph and its next heading.
    paragraph.paragraph_format.space_before = Pt(0 if template else 6)
    paragraph.paragraph_format.space_after = Pt(0)
    run = paragraph.add_run(text.upper() if (level == 1 and upper and bool(PROFILE_CONFIG.get("heading_upper", True))) else text)
    set_font(run, size=BODY_SIZE, bold=True)


def add_bullet(doc: Document, text: str) -> None:
    paragraph = doc.add_paragraph(style="List Bullet")
    paragraph.paragraph_format.line_spacing = 2.0
    run = paragraph.add_run(f"• {text}" if word_template_path() is not None else text)   # a template's bullet style holds no list
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


def add_caption(doc: Document, display: Display, title: str = "", *, compact: bool = False, keep_next: bool = False) -> None:
    """JAMA caption (0.12.0, JL 261023 "the captions are too long"): "Table 1." and the title in bold, the legend after
    it in plain type, single-spaced and a size smaller; it was one italic, double-spaced paragraph."""
    full = display.caption.replace("\x0e", "").replace("\x0f", "").strip()
    head = display.heading.replace("\x0e", "").replace("\x0f", "").strip()
    if head and full.startswith(head):
        legend = full[len(head):].strip()
    else:
        head, legend = full, ""
    if not (title or head):
        return
    paragraph = doc.add_paragraph()
    fmt = paragraph.paragraph_format
    fmt.line_spacing, fmt.space_before, fmt.space_after, fmt.keep_with_next = 1.0, Pt(6), Pt(4), keep_next
    lead = (f"{title}. " if title else "") + head
    set_font(paragraph.add_run(lead.strip()), size=10 if compact else 11, bold=True)
    if legend:
        set_font(paragraph.add_run(" " + legend), size=9 if compact else 10)


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
FLOAT_BOX_MARK = "haipipe-display-float"   # the borderless frame that floats a display to the top of its page


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


def add_figure(doc: Document, display: Display, title: str = "", *, compact: bool = False,
               max_height: float | None = None) -> None:
    base_name = title or Path(display.image_ref).stem or "figure"
    filename = re.sub(r"[^A-Za-z0-9._-]+", "-", base_name).strip("-") + ".png"
    image = ensure_asset(display, filename)
    if image is None:
        add_text(doc, f"{title}: image source not found.", size=10 if compact else 11)
        return
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.keep_with_next = True
    # a template whose Normal style has an EXACT line height clips a picture to that one line (the AITC LOI's
    # v5 template printed only each figure's bottom strip, JL 261113); the picture's own paragraph is single-spaced
    paragraph.paragraph_format.line_spacing = 1.0
    run = paragraph.add_run()
    width = Inches(6.1)
    # the float's own width (\includegraphics[width=0.84\linewidth]) as a share of the text block (JL 261113: the
    # AITC LOI's two figures must fit 2 pages in Word as in LaTeX)
    share = re.search(r"width=([0-9.]+)\\(?:line|text)width", display.block or "")
    if share and doc.sections:
        sec = doc.sections[-1]
        width = int((sec.page_width - sec.left_margin - sec.right_margin) * min(float(share.group(1)), 1.0))
    shape = run.add_picture(str(image), width=width)
    if max_height and shape.height > Inches(max_height):   # a floating display must fit one page with its caption
        ratio = Inches(max_height) / shape.height
        shape.height = Inches(max_height); shape.width = int(shape.width * ratio)
    alt = display.caption or title or display.image_ref
    shape._inline.docPr.set("descr", alt[:500])
    shape._inline.docPr.set("title", filename)
    add_caption(doc, display, title, compact=compact)
    if display.note:
        add_rich_text(doc, display.note, MATH_STORE, size=9 if compact else 10, line_spacing=1.0)


def no_contextual_spacing(p) -> None:
    """Turn off "don't add space between paragraphs of the same style" on one paragraph, so its own space before and
    after print (the Normal style sets it, and Word then ignored a legend's space after, JL 261028)."""
    pPr = p.get_or_add_pPr()
    for old in pPr.findall(qn("w:contextualSpacing")):
        pPr.remove(old)
    el = OxmlElement("w:contextualSpacing"); el.set(qn("w:val"), "0")
    later = {qn(f"w:{n}") for n in ("mirrorIndents", "suppressOverlap", "jc", "textDirection", "textAlignment",
                                     "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange")}
    for i, child in enumerate(pPr):   # schema order: after spacing and ind, before jc
        if child.tag in later:
            pPr.insert(i, el); return
    pPr.append(el)


def body_children(doc: Document) -> list:
    """The body's block elements, without the closing section properties."""
    return [el for el in doc.element.body if el.tag != qn("w:sectPr")]


def float_display_to_top(doc: Document, start: int) -> None:
    """Move what one display wrote (body elements from ``start`` on) into a borderless one-cell floating table pinned
    to the top margin, like LaTeX's [t]: Word sets it at the top of the page where the text reaches it, and the text
    of that page flows on below it (JL 261023: "for all the displays, they are at the top of the page")."""
    moved = body_children(doc)[start:]
    if not moved:
        return
    outer = doc.add_table(rows=1, cols=1)
    tc = outer.cell(0, 0)._tc
    for p in tc.findall(qn("w:p")):
        tc.remove(p)
    for el in moved:
        tc.append(el)
    if moved[-1].tag != qn("w:p"):            # a cell must end with a paragraph
        tc.append(OxmlElement("w:p"))
    tblPr = outer._tbl.tblPr
    pos = OxmlElement("w:tblpPr")
    for k, v in (("leftFromText", "0"), ("rightFromText", "0"), ("topFromText", "0"), ("bottomFromText", "240"),
                 ("vertAnchor", "margin"), ("horzAnchor", "margin"), ("tblpXSpec", "center"), ("tblpYSpec", "top")):
        pos.set(qn(f"w:{k}"), v)
    tblPr.insert(0, pos)
    overlap = OxmlElement("w:tblOverlap"); overlap.set(qn("w:val"), "never")
    tblPr.append(overlap)
    mark = OxmlElement("w:tblDescription"); mark.set(qn("w:val"), FLOAT_BOX_MARK)   # a frame, not a table: not counted
    tblPr.append(mark)
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}"); b.set(qn("w:val"), "nil"); borders.append(b)
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    tblPr.append(borders)
    order = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize", "tblW",
             "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption",
             "tblDescription"]
    rank = {qn(f"w:{n}"): i for i, n in enumerate(order)}
    for child in sorted(list(tblPr), key=lambda c: rank.get(c.tag, len(order))):   # Word reads tblPr in schema order
        tblPr.remove(child); tblPr.append(child)
    set_cell_margins(outer.cell(0, 0), top=0, start=0, bottom=0, end=0)
    cant_split(outer.rows[0])                 # Word split a floating Table 2 over two pages at odd rows
    # the paragraph after a floating table anchors it; an empty one keeps two displays in a row from merging
    anchor = doc.add_paragraph()
    anchor.paragraph_format.space_after = Pt(0)
    anchor.paragraph_format.line_spacing = 1.0
    set_font(anchor.add_run(""), size=1)


def break_before(doc: Document, start: int) -> None:
    """Start what was written from body element ``start`` on a new page: its first paragraph gets "page break
    before". A page-break paragraph after a full-page display spilled to the next page and left it blank."""
    new = body_children(doc)[start:]
    if not new:
        return
    if new[0].tag == qn("w:p"):
        pPr = new[0].get_or_add_pPr()
        node = OxmlElement("w:pageBreakBefore")
        pPr.insert(0, node)
        return
    para = OxmlElement("w:p"); pPr = OxmlElement("w:pPr"); pPr.append(OxmlElement("w:pageBreakBefore")); para.append(pPr)
    new[0].addprevious(para)


def display_is_full_page(display: Display) -> bool:
    """A display that needs most of a page. Word cannot hold such a float back for the next page the way LaTeX does,
    and it splits a tall floating table at odd rows, so a full-page display gets a page of its own instead."""
    if display.kind == "table":
        return len(display.rows or []) > int(PROFILE_CONFIG.get("display_float_max_rows", 25))
    image = display.image_path
    if image is None:
        return False
    try:
        if image.suffix.lower() == ".pdf":   # the page size pdfinfo prints: "Page size: 504 x 612 pts"
            size = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)",
                             subprocess.run(["pdfinfo", str(image)], capture_output=True, text=True).stdout)
            w, h = float(size.group(1)), float(size.group(2))
        else:
            from PIL import Image
            with Image.open(image) as im:
                w, h = im.size
    except Exception:
        return False
    return 6.1 * h / max(w, 1) > float(PROFILE_CONFIG.get("display_float_max_inches", 5.5))


HEADING_COUNTS = [0, 0, 0]   # 0.16.0: the running 1, 1.1, 1.1.1 of profile heading_numbers


def next_heading_number(level: int, first: str = "") -> str:
    """The number a venue's template prints before a heading: 1, 2.1, 2.1.1, or A.1 inside an appendix."""
    index = min(level, 3) - 1
    HEADING_COUNTS[index] += 1
    HEADING_COUNTS[index + 1:] = [0] * (2 - index)
    return ".".join([first or str(HEADING_COUNTS[0])] + [str(n) for n in HEADING_COUNTS[1:index + 1]])


LEGEND_HEADING = re.compile(r"^(?:Extended Data|Supplementary) (?:Fig\.|Figure|Table) \S+\s*\|")


def add_events(doc: Document, events: Iterable[Event], *, include_displays: bool = True, compact: bool = False,
               number_displays: bool = False, main_numbering: bool = False, appendix_letters: bool = False,
               heading_upper: bool = True, number_headings: bool = False,
               line_spacing: float | None = None) -> None:
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
    # a full-page display ends its page: whatever follows starts the next one (page break before, never a break
    # paragraph after, which spilled onto a blank page when the display filled its page; JL 261023)
    break_next = False
    # LEGEND ITEMS (JL 261115, ScalingGlucose Extended Data): a heading that names its own display, "Extended Data
    # Fig. 1 | <title>", with the display right under it and its legend paragraph after, prints as one item on its
    # own page: the display inline (never floated, no numbered caption of its own: the heading already numbers it),
    # then the legend. The Section export (workbench-task-draft export_latex.py) puts it in that order.
    legend_seen = False
    legend_pending = False
    for event in events:
        start = len(body_children(doc))
        new_page = break_next
        break_next = False
        if event.kind != "display":
            legend_pending = False
        if event.kind == "heading":
            title = str(event.value)
            if LEGEND_HEADING.match(title):
                new_page = new_page or legend_seen
                legend_seen = legend_pending = True
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
                HEADING_COUNTS[:] = [0, 0, 0]
                upper = bool(PROFILE_CONFIG.get("appendix_heading_upper", False))
                unnumbered = True
            else:
                upper = heading_upper
                template = word_template_path() is not None
                unnumbered = template and (appendix_letters or not number_headings)
                # 0.16.0: the number printed before a heading. A template's Heading styles draw the main text's numbers; an appendix's A.1 is typed
                if number_headings and ((template and appendix_letters) or (not template and bool(PROFILE_CONFIG.get("heading_numbers", False)))):
                    title = f"{next_heading_number(event.level, chr(ord('A') + letter - 1) if appendix_letters and letter else '')} {title}"
            add_heading(doc, title, event.level, upper=upper, unnumbered=unnumbered)
            if appendix_letters and event.level == 1 and letter == 1 and bool(PROFILE_CONFIG.get("appendix_new_page", False)):
                doc.paragraphs[-1].paragraph_format.page_break_before = True
        elif event.kind == "text":
            add_rich_text(doc, str(event.value), MATH_STORE, size=11 if compact else 12,
                          line_spacing=BODY_SPACING if line_spacing is None else line_spacing)
        elif event.kind == "math":
            add_math_paragraph(doc, str(event.value), size=11 if compact else 12)
        elif event.kind == "code":
            add_code_block(doc, str(event.value))
        elif event.kind == "list":
            for item in event.value:  # type: ignore[union-attr]
                add_bullet(doc, str(item))
        elif event.kind == "display" and include_displays:
            display = event.value
            if isinstance(display, Display) and legend_pending:
                legend_pending = False
                if display.kind == "table":
                    add_table(doc, display, "", compact=compact)
                else:
                    add_figure(doc, display, "", compact=compact, max_height=4.6)   # leaves the double-spaced legend room on the page
            elif isinstance(display, Display):
                title = ""
                if number_displays:
                    counters[display.kind] += 1
                    title = f"{prefixes[display.kind]}{counters[display.kind]}"
                # display_own_page (profile): each main or supplement display alone on its page (JL 261023).
                # display_float (profile, default "top"): a display floats to the top of the page the text reaches it
                # on, like LaTeX's [t]; one that needs most of a page gets a page of its own instead, because Word
                # cannot hold a float back for the next page. "inline" keeps each display where its paragraph ends.
                float_top = str(PROFILE_CONFIG.get("display_float", "top")).lower() == "top"
                full_page = float_top and display_is_full_page(display)
                own_page = bool(PROFILE_CONFIG.get("display_own_page", False)) or full_page
                if float_top and not PROFILE_CONFIG.get("display_own_page") and word_can_measure():
                    # held: placed at the top of the next page after its citing paragraph once Word has laid the
                    # text out (save_docx), so the text fills the page before it, as LaTeX does (JL 261023: "why you
                    # don't put the following paragraphs to fill this margin?"). Floating boxes, the fallback below,
                    # overlapped when two landed on one page.
                    HELD.setdefault(id(doc), []).append({"anchor": last_text_paragraph(doc), "display": display,
                                                         "title": title, "compact": compact, "full_page": full_page})
                    break_next = new_page
                    continue
                new_page = new_page or own_page
                if display.kind == "table":
                    add_table(doc, display, title, compact=compact)
                else:
                    add_figure(doc, display, title, compact=compact, max_height=6.4 if own_page else None)
                if float_top and not own_page:
                    float_display_to_top(doc, start)
                elif not own_page:
                    # inline: a clear gap above and below, so the legend never reads as the next body paragraph
                    # (JL 261028: Figure 1's legend ran straight into the Results text)
                    pars = [el for el in body_children(doc)[start:] if el.tag == qn("w:p")]
                    if pars:
                        Paragraph(pars[0], doc._body).paragraph_format.space_before = Pt(12)
                        Paragraph(pars[-1], doc._body).paragraph_format.space_after = Pt(18)
                        for el in (pars[0], pars[-1]):   # the style's contextual spacing drops space between Normal paragraphs
                            no_contextual_spacing(el)
                break_next = own_page
        if new_page:
            break_before(doc, start)


# ---- full-page displays held for the next page (0.12.0) -------------------------------------------------------
# Word cannot hold a display back while the text keeps filling the page, the way LaTeX does with a [p] float. So a
# display that needs a whole page is left out at first; Microsoft Word lays the document out and reports where the
# page that holds the citing paragraph ends; the display is then put at that boundary on a page of its own, splitting
# the paragraph that crosses it, and the text goes on after it. Without Word (no Mac, a test) it prints at once.
MSWORD_APP = Path("/Applications/Microsoft Word.app")
WORD_BOX = Path.home() / "Library" / "Containers" / "com.microsoft.Word" / "Data" / "Documents" / "haipipe-measure"
HELD: dict[int, list[dict]] = {}


def word_can_measure() -> bool:
    if os.environ.get("HAIPIPE_WORD_DRAFT") == "1":   # build.py --word-draft (JL 261104): floats, no measuring; Word sets
        return False                                  # each display at the top of the page its citing text reaches
    return (sys.platform == "darwin" and MSWORD_APP.exists() and os.environ.get("HAIPIPE_WORD_PREVIEW") != "html"
            and "PYTEST_CURRENT_TEST" not in os.environ)


def element_text(el) -> str:
    return "".join(node.text or "" for node in el.iter(qn("w:t")))


def last_text_paragraph(doc: Document):
    for el in reversed(body_children(doc)):
        if el.tag == qn("w:p") and len(element_text(el).strip()) >= 25:
            return el
    return None


def _squash(text: str) -> tuple[str, list[int]]:
    """the text without whitespace, and for each kept character its index in the original"""
    keep = [(c, i) for i, c in enumerate(text) if not c.isspace()]
    return "".join(c for c, _ in keep), [i for _, i in keep]


def _applescript_string(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def word_running() -> bool:
    return subprocess.run(["pgrep", "-x", "Microsoft Word"], capture_output=True).returncode == 0


WORD_STUCK = "Word did not answer"     # build_delivery.py finds this line in the step's output and warns


def word_answers(wait: int = 30) -> bool:
    """A quick question only a working Word can answer. A stuck Word (b16.j02-s22, 261104: its main thread on a lock, 0%
    CPU) let every display wait out AppleScript's 120 seconds and still fall back, about 28 minutes a paper, in silence."""
    script = f'with timeout of {wait} seconds\ntell application "Microsoft Word" to get name of documents\nend timeout'
    try:
        return subprocess.run(["osascript", "-e", script], capture_output=True, timeout=wait + 10).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def word_page_boundaries(path: Path, anchors: list[str]) -> list[str | None]:
    """For each anchor ("E|text": the page the text ends on; "S|text": the page it starts on), the ~120 characters
    Word lays out just before the end of that page (paragraph marks as <P>, cell marks as <C>), or None."""
    WORD_BOX.mkdir(parents=True, exist_ok=True)
    copy = WORD_BOX / path.name
    shutil.copy2(path, copy)
    # "E|3|text": the 3rd match of text (the Abstract repeats Results phrases, so the first match can be wrong)
    finds = ", ".join(_applescript_string(a.split("|", 2)[0] + "|" + a.split("|", 2)[1] + "|"
                                          + a.split("|", 2)[2].replace("^", "^^")) for a in anchors)
    script = f"""
on rep(t, a, b)
  set AppleScript's text item delimiters to a
  set xs to text items of t
  set AppleScript's text item delimiters to b
  set r to xs as text
  set AppleScript's text item delimiters to ""
  return r
end rep
tell application "Microsoft Word"
  set d to open file name "{copy}"
  repaginate d
  set n to end of content of text object of d
  set out to ""
  repeat with a in {{{finds}}}
   try
    home key selection move unit a story
    set q to a as text
    set AppleScript's text item delimiters to "|"
    set parts to text items of q
    set mode to item 1 of parts
    set k to (item 2 of parts) as integer
    set q to (items 3 thru -1 of parts) as text
    set AppleScript's text item delimiters to ""
    set ok to false
    repeat with i from 1 to k
      if i > 1 then set selection start of selection to (selection end of selection)
      set ok to (execute find (find object of selection) find text q match case true wrap find find stop with match forward)
      if not ok then exit repeat
    end repeat
    if ok then
      if mode is "S" then
        set fe to selection start of selection
      else
        set fe to selection end of selection
      end if
      set pe to ((get range information (create range d start fe end fe) information type active end page number) as integer)
      set lo to fe
      set hi to n
      if ((get range information (create range d start (hi - 1) end (hi - 1)) information type active end page number) as integer) > pe then
        repeat while hi - lo > 1
          set m to (lo + hi) div 2
          if ((get range information (create range d start m end m) information type active end page number) as integer) > pe then
            set hi to m
          else
            set lo to m
          end if
        end repeat
        set s to hi - 120
        if s < 0 then set s to 0
        set bt to content of (create range d start s end hi)
        set bt to my rep(my rep(bt, return, "<P>"), (ASCII character 7), "<C>")
        set out to out & "OK" & tab & bt & linefeed
      else
        set out to out & "END" & linefeed
      end if
    else
      set out to out & "MISS" & linefeed
    end if
   on error e
    set out to out & "ERR " & e & linefeed
   end try
  end repeat
  close d saving no
end tell
return out
"""
    try:
        r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=600)
    finally:
        copy.unlink(missing_ok=True)
    if r.returncode != 0:
        print(f"Word could not lay out {path.name}: {r.stderr.strip()[:300]}", file=sys.stderr)
        return [None] * len(anchors)
    lines = [ln for ln in r.stdout.split("\n") if ln.strip()]
    for ln in lines:
        if not ln.startswith("OK\t"):
            print(f"Word page end for {path.name}: {ln[:200]}", file=sys.stderr)
    found = [ln.split("\t", 1)[1] if ln.startswith("OK\t") else None for ln in lines]
    return (found + [None] * len(anchors))[:len(anchors)]


def set_page_break_before(el) -> None:
    if el is None:
        return
    if el.tag == qn("w:p"):
        pPr = el.find(qn("w:pPr"))
        if pPr is None:
            pPr = OxmlElement("w:pPr"); el.insert(0, pPr)
        if pPr.find(qn("w:pageBreakBefore")) is None:
            pPr.insert(0, OxmlElement("w:pageBreakBefore"))
        return
    para = OxmlElement("w:p"); pPr = OxmlElement("w:pPr"); pPr.append(OxmlElement("w:pageBreakBefore")); para.append(pPr)
    el.addprevious(para)


def split_paragraph(p_el, offset: int):
    """Split a body paragraph after `offset` characters of its text; the second part carries on the same paragraph
    (no first-line indent) and is returned."""
    new_p = OxmlElement("w:p")
    pPr = p_el.find(qn("w:pPr"))
    if pPr is not None:
        new_pPr = deepcopy(pPr)
        ind = new_pPr.find(qn("w:ind"))
        if ind is None:
            ind = OxmlElement("w:ind"); new_pPr.append(ind)
        ind.set(qn("w:firstLine"), "0")
        if ind.get(qn("w:hanging")) is not None:
            del ind.attrib[qn("w:hanging")]
        new_p.append(new_pPr)
    else:
        new_pPr = OxmlElement("w:pPr"); ind = OxmlElement("w:ind"); ind.set(qn("w:firstLine"), "0")
        new_pPr.append(ind); new_p.append(new_pPr)
    count, moving = 0, False
    for child in [c for c in p_el if c.tag != qn("w:pPr")]:
        if moving:
            new_p.append(child)
            continue
        text = element_text(child)
        if count + len(text) <= offset:
            count += len(text)
            continue
        k = offset - count
        if child.tag == qn("w:r") and 0 < k < len(text):
            tail = deepcopy(child)
            ts, tail_ts = child.findall(qn("w:t")), tail.findall(qn("w:t"))
            if len(ts) == 1:
                ts[0].text = text[:k]
                tail_ts[0].text = text[k:].lstrip()
                for node in (ts[0], tail_ts[0]):
                    node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                new_p.append(tail)
                moving = True
                continue
        new_p.append(child)   # the split falls at this child's start
        moving = True
    p_el.addnext(new_p)
    return new_p


def boundary_target(anchor, before: str | None):
    """The body element a held display goes in front of, splitting a paragraph when the page ends inside it."""
    if anchor is None or before is None:
        return None
    following = [anchor]
    while following[-1].getnext() is not None and following[-1].getnext().tag != qn("w:sectPr"):
        following.append(following[-1].getnext())
    at_par_start = before.endswith("<P>") or before.endswith("<C>")
    segments = [s for s in re.split(r"<P>|<C>", before) if s.strip()]
    if not segments:
        return None
    seg, _ = _squash(segments[-1])
    if len(seg) < 8:
        return None
    for el in following:
        squashed, index = _squash(element_text(el))
        if at_par_start:
            if el.tag == qn("w:p") and squashed.endswith(seg):
                return el.getnext()
        elif el.tag == qn("w:p"):
            pos = squashed.find(seg)
            if pos >= 0:
                end = index[pos + len(seg) - 1] + 1
                full = element_text(el)
                if end >= len(full.rstrip()):
                    return el.getnext()
                # split only where a sentence ends, never inside one (JL 261028: a display cut a sentence in two);
                # the page then ends on a full stop and the display opens the next page, as LaTeX does. When the
                # page ends inside the paragraph's first sentence, the display goes in front of the paragraph.
                stops = [m.end() for m in re.finditer(r"[.?!][)\]\"”’]*\s+", full) if m.end() <= end]
                if not stops:
                    return el
                return split_paragraph(el, stops[-1])
    return None


def is_heading1(p_el) -> bool:
    """A paragraph set in the Heading 1 style: a main Section or an Appendix opens here."""
    pPr = p_el.find(qn("w:pPr"))
    style = pPr.find(qn("w:pStyle")) if pPr is not None else None
    return style is not None and style.get(qn("w:val")) in {"Heading1", "Heading 1", "Subtitle"}   # Subtitle: a template's REFERENCES, APPENDIX


def _body_index(el) -> int:
    body = el.getparent()
    return list(body).index(el) if body is not None else -1


def save_docx(doc: Document, path: Path) -> None:
    """Save; then place each held display, in order, at the top of the page after the one its citing paragraph ends
    on, as Microsoft Word lays the document out, and save again. A display cited before the end of the one placed
    just before it goes to the page after that one, so the order of the displays and their citations holds."""
    doc.save(path)
    held = HELD.pop(id(doc), [])
    if not held:
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from word_lock import word_turn
    with word_turn() as turn:      # builds take turns in Word, for the whole document (b16.j02-s22)
        place_held(doc, path, held, turn)


def place_held(doc: Document, path: Path, held: list, turn: bool) -> None:
    was_running, placed, last = word_running(), 0, None
    answers = turn and word_answers()
    if not answers:
        print(f"{WORD_STUCK} in 30 seconds: {Path(path).name}'s {len(held)} display(s) go right after their citing "
              "paragraphs, not at page tops. Restart Word and build again.", file=sys.stderr)
    try:
        for h in held:
            anchor, mode = h["anchor"], "E"
            if last is not None and (anchor is None or _body_index(anchor) < _body_index(last)):
                anchor, mode = last.getnext(), "S"     # after the display placed just before
                while anchor is not None and not (anchor.tag == qn("w:p") and len(element_text(anchor).strip()) >= 25):
                    anchor = anchor.getnext()
            target, measured = None, False
            if anchor is not None:
                text = element_text(anchor).strip()
                snippet = text[:50] if mode == "S" else text[-60:]
                # which match is the anchor's own: count the matches in the body up to and including it
                k = 0
                for el in body_children(doc):
                    k += element_text(el).count(snippet)
                    if el is anchor:
                        break
                doc.save(path)
                before = word_page_boundaries(Path(path), [f"{mode}|{max(k, 1)}|{snippet}"])[0] if answers else None
                target = boundary_target(anchor, before)
                placed += target is not None
                measured = target is not None
                if target is None:                   # Word could not say: right after the citing paragraph
                    target = anchor.getnext()
                # a display never crosses into the next Section or Appendix: if a Heading 1 lies between its citing
                # paragraph and the measured page, it goes in front of that heading, as LaTeX's \clearpage flushes
                # floats before the next appendix (261101: Table B1 printed under Appendix C, Table C2 under D)
                el = anchor.getnext()
                while el is not None and el is not target and el.tag != qn("w:sectPr"):
                    if el.tag == qn("w:p") and is_heading1(el):
                        target = el
                        break
                    el = el.getnext()
            start = len(body_children(doc))
            display = h["display"]
            if display.kind == "table":
                add_table(doc, display, h["title"], compact=h["compact"])
            else:
                add_figure(doc, display, h["title"], compact=h["compact"], max_height=6.4 if h["full_page"] else None)
            moved = body_children(doc)[start:]
            pars = [el for el in moved if el.tag == qn("w:p")]
            if pars:   # a clear gap under the legend, so it never reads as the body text that follows (JL 261028)
                Paragraph(pars[-1], doc._body).paragraph_format.space_after = Pt(18)
                no_contextual_spacing(pars[-1])
            if target is not None and target.tag != qn("w:sectPr"):
                for el in moved:
                    target.addprevious(el)
                # a figure that fills its page sends the text on to the next page; after a table, or a short
                # figure, the text goes on below it
                if h["full_page"] and display.kind != "table":
                    set_page_break_before(target)
            # a display placed at a page Word measured starts that page; one placed by the fallback (Word could not
            # find its citing paragraph) stays right after it with no break, so it never strands a page of two lines
            if measured or h["full_page"]:
                set_page_break_before(moved[0])
            last = moved[-1]
    finally:
        if not was_running and word_running():
            try:   # never with a document open: a person may have opened one during the build
                subprocess.run(["osascript", "-e", 'tell application "Microsoft Word" to if (count of documents) is 0 then quit saving no'],
                               capture_output=True, timeout=30)
            except subprocess.TimeoutExpired:
                pass
            for _ in range(40):   # wait until Word has gone, or the preview step takes it for the user's own Word
                if not word_running():
                    break
                import time; time.sleep(0.25)
    doc.save(path)
    print(f"{Path(path).name}: {len(held)} display(s) placed at the top of a page; {placed} where Word ended the page")


def add_supplement_contents(doc: Document, events: list[Event]) -> None:
    """The first-page list of a JAMA supplement: each section heading, then each table and figure by its caption."""
    add_text(doc, "This supplemental material has been provided by the authors to give readers additional information "
                  "about their work.", size=11, line_spacing=1.5, before=12)
    prefixes = {"table": str(PROFILE_CONFIG.get("supplement_table_prefix", "Table S")),
                "figure": str(PROFILE_CONFIG.get("supplement_figure_prefix", "Figure S"))}
    counters = {"table": 0, "figure": 0}
    for event in events:
        if event.kind == "heading" and event.level <= 2:
            add_text(doc, str(event.value), size=11, line_spacing=1.15)
        elif event.kind == "display" and isinstance(event.value, Display):
            counters[event.value.kind] += 1     # the same count add_events prints, so the list names the same labels
            label = f"{prefixes[event.value.kind]}{counters[event.value.kind]}."
            # the title, not the legend under it: a whole caption made a list of paragraphs
            add_text(doc, f"    {label} {event.value.heading or event.value.caption}".rstrip(), size=10, line_spacing=1.15)


def restyle_runs(doc: Document, font: str, body_size: float) -> None:
    """Set every run, tables included, in `font`; body text at `body_size` (bold headings keep theirs up to 12 pt)."""
    def runs():
        for p in doc.paragraphs:
            yield from p.runs
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        yield from p.runs
    for run in runs():
        run.font.name = font
        rpr = run._element.get_or_add_rPr()
        fonts = rpr.find(qn("w:rFonts"))
        if fonts is None:
            fonts = OxmlElement("w:rFonts")
            rpr.append(fonts)
        for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            fonts.set(qn(attr), font)
        if run.bold:
            run.font.size = Pt(min(run.font.size.pt if run.font.size else 12, 12))
        else:
            run.font.size = Pt(min(run.font.size.pt if run.font.size else body_size, body_size))


def add_abstract(doc: Document, block: str) -> None:
    add_heading(doc, str(PROFILE_CONFIG.get("abstract_heading", "ABSTRACT")), 1,
                upper=bool(PROFILE_CONFIG.get("abstract_heading_upper", True)), unnumbered=True)
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
        "title":       lambda: ((add_text(doc, title, size=doc.styles["Title"].font.size.pt, bold=True,
                                          align=WD_ALIGN_PARAGRAPH.CENTER, style="Title", line_spacing=2.0, before=0, after=0)
                             if word_template_path() is not None else
                             add_text(doc, title, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                                      style="Title", line_spacing=1.0, before=48, after=36))
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


_load_part("venue_jama.py")   # labelled_blocks, jama_parts, add_byline, add_jama_title_page, build_jama_internal_medicine


def initials(author: str) -> str:
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", author)
    return "".join(token[0].upper() for token in tokens if token)


def format_authors(author_field: str) -> str:
    if corporate_author(author_field):
        return corporate_author(author_field)
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


_BBL: dict[str, str] | None = None


def bbl_references() -> dict[str, str]:
    """The reference list LaTeX itself printed (master.bbl, written by BibTeX with the venue's .bst), one text per key.
    0.12.0 (JL 261023: "can't LaTeX do this?"): Word reuses it, so both copies print the same references."""
    global _BBL
    if _BBL is None:
        _BBL = {}
        bbl = next((p for p in (MASTER.with_suffix(".bbl"), LATEX_ROOM / "master.bbl") if p.is_file()), None)
        if bbl is not None:
            for key, body in re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})",
                                        bbl.read_text(encoding="utf-8", errors="replace"), re.S):
                body = re.sub(r"\\url\{([^}]*)\}", r"\1", body.replace("\\newblock", " "))
                body = re.sub(r"\\penalty-?\d+\s*", "", body)   # 0.12.3: unsrtnat's "175\\penalty0 (2)" printed "1750 (2)"
                body = body.replace('{\\"\\i}', "ï").replace("\\i", "i")
                text = re.sub(r"\s+", " ", latex_to_text(body)).strip()
                if text:
                    _BBL[key] = text
    return _BBL


def format_reference(key: str) -> str:
    if key in bbl_references():
        return bbl_references()[key]
    fields = BIB[key]
    authors = format_authors(fields.get("author", ""))
    title = latex_to_text(fields.get("title", ""))
    journal = latex_to_text(fields.get("journal", fields.get("booktitle", "")))
    year = latex_to_text(fields.get("year", ""))
    volume = latex_to_text(fields.get("volume", ""))
    pages = latex_to_text(fields.get("pages", ""))
    doi = latex_to_text(fields.get("doi", ""))
    # AMA (JAMA): "Journal. Year;Volume(Issue):Pages." (0.12.0, JL 261023: Word printed "JAMA. 2020 323 863–884")
    number = latex_to_text(fields.get("number", fields.get("issue", "")))
    pages = re.sub(r"\s*(--|–|—)\s*", "-", pages)
    cite = year
    if volume:
        cite += f";{volume}" + (f"({number})" if number else "") + (f":{pages}" if pages else "")
    elif pages:
        cite += f":{pages}"
    pieces = [part.strip().rstrip(".") for part in (authors, title, journal) if part and part.strip()]
    if cite:
        pieces.append(cite)
    if doi:
        pieces.append("doi:" + doi)
    return ". ".join(pieces).rstrip(".") + "."


def apa_authors(author_field: str) -> str:
    """Barnett, M. L., Olenski, A. R., & Jena, A. B."""
    if corporate_author(author_field):
        return corporate_author(author_field)
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
    add_heading(doc, str(PROFILE_CONFIG.get("references_heading", "REFERENCES")), 1, unnumbered=True)
    if bool(PROFILE_CONFIG.get("references_new_page", False)):
        doc.paragraphs[-1].paragraph_format.page_break_before = True
    if author_date_style():
        # alphabetical by first author, no numbers: the order a reader looks a name up in
        for key in sorted(CITATION_NUMBERS, key=lambda k: (surname_of(BIB[k].get("author", "")).lower(),
                                                           latex_to_text(BIB[k].get("year", "")))):
            template = word_template_path() is not None
            paragraph = doc.add_paragraph(style="No Spacing" if template else "Normal")
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.left_indent = Inches(0.5)
            paragraph.paragraph_format.first_line_indent = Inches(-0.5)
            set_font(paragraph.add_run(format_reference_apa(key)), size=12 if template else 11)
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


_load_part("docx_receipts.py")   # word_count, write_section_snapshots, evidence_preflight, source_manifest, write_common_receipts


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
    # a paper-owned head may write \title{\thetitle}, a macro this reader cannot expand: use the
    # configured title then (0.9.1)
    title = latex_to_text(extract_command(raw_master, "title")) or str(PAPER_CONFIG.get("title", ""))
    author = latex_to_text(extract_command(raw_master, "author"))
    body = clean_fragment(raw_master, MASTER.parent, remove_abstract=False)
    body = body.split(r"\begin{document}", 1)[-1].split(r"\end{document}", 1)[0]
    register_labels(body)

    abstract_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, re.S)
    # a grant (a Grant-<Slug> Board's LOI or Project Statement) has no abstract (JL 261112): the text then starts
    # right after the title, and no Abstract heading is printed
    no_abstract = abstract_match is None
    if no_abstract:
        title_match = re.search(r"\\maketitle\b", body)
        if title_match is None:
            raise RuntimeError("Master manuscript has neither an abstract environment nor \\maketitle")
        abstract_match = title_match
    abstract = "" if no_abstract else abstract_match.group(1)
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

    main_doc = new_main_document()
    add_title_page(main_doc, title, running_title, word_count(main_events), len(main_tables), len(main_figures), author)
    if not no_abstract:
        add_abstract(main_doc, abstract)
    # abstract_own_page (profile): the abstract and keywords end their page and the text starts on a new one (JL 261023)
    if not no_abstract and (_front_matter_on_one_page() or bool(PROFILE_CONFIG.get("abstract_own_page", False))):
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
               number_displays=inline_displays, main_numbering=True, number_headings=True)
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
                   appendix_letters=True, number_headings=True)
    save_docx(main_doc, MAIN_PATH)
    if appendices_in_main:
        for stale in (SUPP_PATH, SUPP_PDF_PATH):
            if stale.exists():
                stale.unlink()
        pdf_report = render_submission_pdfs()
        write_common_receipts(main_events, main_displays, supplement_events, running_title, evidence, pdf_report)
        return MAIN_PATH, None

    supp_doc = Document()
    # supplement_line_spacing (profile or paper-build.toml): the supplement's text spacing; Nature's Extended Data
    # legends are not judged on it, and single spacing keeps a long table and its legend on one page (261115)
    supp_spacing = float(PROFILE_CONFIG.get("supplement_line_spacing", 1.5))
    configure_document(supp_doc, body_size=11, line_spacing=supp_spacing)
    add_text(supp_doc, title, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(supp_doc, str(PROFILE_CONFIG.get("supplement_title", "ONLINE-ONLY SUPPLEMENTAL MATERIAL")), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(supp_doc, "[AUTHOR ACTION REQUIRED: confirm that all supplement citations, table labels, and figure labels match the final main manuscript]", size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    supp_doc.add_page_break()
    add_events(supp_doc, supplement_events, include_displays=True, compact=True, number_displays=True,
               appendix_letters=True,
               line_spacing=supp_spacing if "supplement_line_spacing" in PROFILE_CONFIG else None)
    save_docx(supp_doc, SUPP_PATH)

    pdf_report = render_submission_pdfs()
    write_common_receipts(main_events, main_displays, supplement_events, running_title, evidence, pdf_report)
    # 0.7.1 tooth (Paper-Example-Misq, JL 260908): every table float the master prints must
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
    return (xml.count("<w:tbl>") - xml.count(f'<w:tblDescription w:val="{CODE_BOX_MARK}"/>')
            - xml.count(f'<w:tblDescription w:val="{FLOAT_BOX_MARK}"/>'))   # 0.12.0: the frame of a floated display


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
