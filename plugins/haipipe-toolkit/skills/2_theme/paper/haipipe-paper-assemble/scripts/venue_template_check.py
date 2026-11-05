#!/usr/bin/env python3
"""Does a built manuscript follow the venue's own template? (JL 261104)

JL: "I think this should be the checklist for the /haipipe-paper-assemble to make sure they follow the venue
template". Reads the template the venue publishes and the file the build wrote, then prints one row per rule:
what the template sets, what the build has. It changes nothing. A difference a person chose stays listed, under
`accepted` in paper-build.toml's [venue_template].

  venue_template_check.py --word-template T.docx --docx B.docx [--docx-pdf B.pdf]
                          [--latex-template T.tex --head head.tex --latex-pdf B.pdf] [--accept "rule"]...
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def _row(rule, template, built, accepted=()):
    same = template == built
    return {"rule": rule, "template": template, "built": built,
            "state": "same" if same else ("accepted" if rule in accepted else "differs")}


def _size(paragraph):
    for run in paragraph.runs:
        if run.text.strip() and run.font.size:
            return run.font.size.pt
    style = paragraph.style
    while style is not None:
        if style.font.size:
            return style.font.size.pt
        style = style.base_style
    return None


def _spacing(paragraph):
    value = paragraph.paragraph_format.line_spacing
    style = paragraph.style
    while value is None and style is not None:
        value = style.paragraph_format.line_spacing
        style = style.base_style
    return value


def _alignment(paragraph):
    value = paragraph.paragraph_format.alignment
    style = paragraph.style
    while value is None and style is not None:
        value = style.paragraph_format.alignment
        style = style.base_style
    return "center" if value == 1 else "left"


def _bold(paragraph):
    runs = [r for r in paragraph.runs if r.text.strip()]
    if runs and runs[0].bold is not None:
        return bool(runs[0].bold)
    style = paragraph.style
    while style is not None:
        if style.font.bold is not None:
            return bool(style.font.bold)
        style = style.base_style
    return False


def _numbered(paragraph):
    """A number the style draws (a Word numbered list) or one typed at the head of the text."""
    from docx.oxml.ns import qn
    style = paragraph.style
    while style is not None:
        ppr = style.element.find(qn("w:pPr"))
        if ppr is not None and ppr.find(qn("w:numPr")) is not None:
            return True
        style = style.base_style
    return bool(re.match(r"\d+(\.\d+)*\s", paragraph.text.strip()))


def _case(text):
    letters = re.sub(r"[^A-Za-z]", "", text)
    return "caps" if letters and letters == letters.upper() else "title"


def _starts_page(paragraphs, index):
    from docx.oxml.ns import qn
    paragraph = paragraphs[index]
    if paragraph.paragraph_format.page_break_before:
        return True
    if paragraph._p.findall(f".//{qn('w:lastRenderedPageBreak')}"):
        return True
    body = list(paragraph._p.getparent())
    position = body.index(paragraph._p)
    return position > 0 and bool(body[position - 1].findall(f".//{qn('w:br')}[@{qn('w:type')}='page']"))


def _find(paragraphs, word):
    for index, paragraph in enumerate(paragraphs):
        if paragraph.text.strip().upper() == word:
            return index
    return None


def _first_heading(paragraphs, level, after=0):
    for paragraph in paragraphs[after:]:
        if paragraph.style.name == f"Heading {level}" and not re.search(r"abstract|references", paragraph.text, re.I):
            return paragraph
    return None


def _is_appendix_heading(paragraph):
    """A heading, never a body sentence that opens with "Appendix C lists...", the build's first false alarm."""
    return paragraph.text.strip().upper().startswith("APPENDIX") and paragraph.style.name != "Normal"


def word_rows(template_path, built_path, accepted=()):
    from docx import Document
    template, built = Document(str(template_path)), Document(str(built_path))
    tp = [p for p in template.paragraphs if p.text.strip()]
    bp = [p for p in built.paragraphs if p.text.strip()]
    rows = []

    def add(rule, make, *_):
        try:
            a, b = make(tp), make(bp)
        except (AttributeError, IndexError, TypeError, StopIteration):
            a, b = "not found", "not found"
        rows.append(_row(rule, a, b, accepted))

    def section(doc, name):
        return round(getattr(doc.sections[0], name).inches, 2)

    for name, rule in (("page_width", "page width (in)"), ("page_height", "page height (in)"),
                       ("left_margin", "left margin (in)"), ("right_margin", "right margin (in)"),
                       ("top_margin", "top margin (in)"), ("bottom_margin", "bottom margin (in)")):
        rows.append(_row(rule, section(template, name), section(built, name), accepted))
    normal = lambda d: d.styles["Normal"]
    rows.append(_row("body font", normal(template).font.name, normal(built).font.name, accepted))
    rows.append(_row("body size (pt)", normal(template).font.size.pt, normal(built).font.size.pt, accepted))
    rows.append(_row("body line spacing", normal(template).paragraph_format.line_spacing,
                     normal(built).paragraph_format.line_spacing, accepted))
    add("title size (pt)", lambda ps: _size(ps[0]))
    add("title bold", lambda ps: _bold(ps[0]))
    add("title alignment", lambda ps: _alignment(ps[0]))
    add("abstract heading case", lambda ps: _case(ps[_find(ps, "ABSTRACT")].text))
    add("abstract line spacing", lambda ps: _spacing(ps[_find(ps, "ABSTRACT") + 1]))
    add("keywords line spacing", lambda ps: _spacing(next(p for p in ps if p.text.strip().lower().startswith("keywords"))))
    add("major heading alignment", lambda ps: _alignment(_first_heading(ps, 1)))
    add("major heading bold", lambda ps: _bold(_first_heading(ps, 1)))
    add("major heading case", lambda ps: _case(_first_heading(ps, 1).text))
    add("major heading numbered", lambda ps: _numbered(_first_heading(ps, 1)))
    add("first subhead alignment", lambda ps: _alignment(_first_heading(ps, 2)))
    add("first subhead numbered", lambda ps: _numbered(_first_heading(ps, 2)))
    add("references heading case", lambda ps: _case(ps[_find(ps, "REFERENCES")].text))
    add("references line spacing", lambda ps: _spacing(ps[_find(ps, "REFERENCES") + 1]))
    add("references hanging indent (in)",
        lambda ps: round(-ps[_find(ps, "REFERENCES") + 1].paragraph_format.first_line_indent.inches, 1)
        if ps[_find(ps, "REFERENCES") + 1].paragraph_format.first_line_indent is not None
        else round(_hanging(ps[_find(ps, "REFERENCES") + 1]), 1))
    add("references size (pt)", lambda ps: _size(ps[_find(ps, "REFERENCES") + 1]))
    add("references start a new page", lambda ps: _starts_page(ps, _find(ps, "REFERENCES")))
    add("appendix heading case", lambda ps: _case(next(p for p in ps if _is_appendix_heading(p)).text))
    add("appendix starts a new page",
        lambda ps: _starts_page(ps, next(i for i, p in enumerate(ps) if _is_appendix_heading(p))))
    for name in ("Normal", "Title", "Subtitle", "Heading 1", "Heading 2", "Heading 3", "No Spacing"):
        rows.append(_row(f"style {name}", "template's", "template's" if _style(template, name) == _style(built, name) else "changed", accepted))
    rows.append(_row("footer page number", _page_number(template), _page_number(built), accepted))
    return rows


def _style(doc, name):
    """A style's paragraph and font settings, to see that a build kept the template's own."""
    from docx.oxml.ns import qn
    from lxml import etree
    try:
        element = doc.styles[name].element
    except KeyError:
        return None
    return [etree.tostring(child, method="c14n") for tag in ("w:pPr", "w:rPr") for child in element.findall(qn(tag))]


def _page_number(doc):
    return "PAGE" in "".join(doc.sections[0].footer._element.itertext())


def _hanging(paragraph):
    from docx.oxml.ns import qn
    ind = paragraph._p.find(f"{qn('w:pPr')}/{qn('w:ind')}")
    return int(ind.get(qn("w:hanging"), 0)) / 1440 if ind is not None else 0


def _pdf_text(pdf, first, last):
    if not shutil.which("pdftotext"):
        return None
    return subprocess.run(["pdftotext", "-f", str(first), "-l", str(last), "-layout", str(pdf), "-"],
                          capture_output=True, text=True).stdout


def page_rows(label, pdf, accepted=()):
    """What every template with a Keywords line asks: title, abstract, keywords on page 1, the text from page 2."""
    one, two = _pdf_text(pdf, 1, 1), _pdf_text(pdf, 2, 2)
    if one is None:
        return [{"rule": f"{label} page 1", "template": "-", "built": "pdftotext missing", "state": "not checked"}]
    head = next((line.strip() for line in two.splitlines() if line.strip()), "")
    return [_row(f"{label} keywords on page 1", True, "keywords" in one.lower(), accepted),
                _row(f"{label} page 2 opens with a major heading", True, bool(re.fullmatch(r"[\d. ]*[A-Z][A-Z ]+", head)), accepted)]


LENGTHS = ("topmargin", "oddsidemargin", "evensidemargin", "textwidth", "textheight")


def _tex_setting(tex, name):
    match = re.search(r"\\setlength\{\\%s\}\{([^}]+)\}" % name, tex)
    return match.group(1) if match else "not set"


def latex_rows(template_path, head_path, pdf=None, accepted=()):
    template = Path(template_path).read_text(encoding="utf-8", errors="replace")
    head = Path(head_path).read_text(encoding="utf-8", errors="replace")
    rows = [_row(name, _tex_setting(template, name), _tex_setting(head, name), accepted) for name in LENGTHS]
    klass = lambda t: (re.search(r"\\documentclass(\[[^\]]*\])?\{[^}]+\}", t) or [None])[0]
    rows.append(_row("document class", klass(template), klass(head), accepted))
    stretch = lambda t: (re.search(r"\\baselinestretch\}\{([\d.]+)\}", t) or [None, "not set"])[1]
    rows.append(_row("body line stretch", stretch(template), stretch(head), accepted))
    def abstract(t):
        match = re.search(r"abstract\}[^\n]*?\\baselinestretch\}\{([\d.]+)\}", t) or \
                re.search(r"\\begin\{abstract\}\s*\\renewcommand\{\\baselinestretch\}\{([\d.]+)\}", t)
        return match.group(1) if match else "not set"
    rows.append(_row("abstract line stretch", abstract(template), abstract(head), accepted))
    if pdf is not None and Path(pdf).is_file():
        rows += page_rows("LaTeX", pdf, accepted)
        if "APPENDIX" in template:
            printed = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout if shutil.which("pdftotext") else ""
            rows.append(_row("LaTeX appendix heading says APPENDIX", True, bool(re.search(r"^\s*APPENDIX\b", printed, re.M)), accepted))
        fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout if shutil.which("pdffonts") else ""
        if fonts:
            wants_times = "{times}" in template
            rows.append(_row("LaTeX body font is Times", wants_times, bool(re.search(r"times", fonts, re.I)), accepted))
    return rows


def report(word_template=None, docx=None, docx_pdf=None, latex_template=None, head=None, latex_pdf=None, accepted=()):
    result = {}
    if word_template and docx and Path(docx).is_file():
        result["word"] = word_rows(word_template, docx, accepted)
        if docx_pdf and Path(docx_pdf).is_file():
            result["word"] += page_rows("Word", docx_pdf, accepted)
    if latex_template and head:
        result["latex"] = latex_rows(latex_template, head, latex_pdf, accepted)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--word-template"); parser.add_argument("--docx"); parser.add_argument("--docx-pdf")
    parser.add_argument("--latex-template"); parser.add_argument("--head"); parser.add_argument("--latex-pdf")
    parser.add_argument("--accept", action="append", default=[])
    args = parser.parse_args(argv)
    result = report(args.word_template, args.docx, args.docx_pdf, args.latex_template, args.head, args.latex_pdf, args.accept)
    differs = 0
    marks = {"same": "✅", "differs": "❌", "accepted": "🙋", "not checked": "⬜"}
    for lane, rows in result.items():
        print(f"== {lane}")
        for row in rows:
            differs += row["state"] == "differs"
            print(f"{marks[row['state']]} {row['rule']}: template {row['template']} · built {row['built']}")
    print(f"{differs} difference(s) from the venue template")
    return 1 if differs else 0


if __name__ == "__main__":
    sys.exit(main())
