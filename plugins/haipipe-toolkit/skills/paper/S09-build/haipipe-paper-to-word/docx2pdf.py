#!/usr/bin/env python3
"""docx2pdf.py -- render a .docx we generated into a PDF, comments and all.

WHY NOT textutil, WHICH IS INSTALLED. It converts CONTENT and has no concept of
a `w:comment`. Measured 2026-07-27 on `S-Main-all.docx`: 239 anchored comments
became 0, 3 embedded images became 0, and the double spacing was dropped, so the
same text fitted in 13 pages instead of 47. For a file whose whole purpose is
carrying evidence to a coauthor, that is not a lossy render, it is a different
document.

WHY NOT LibreOffice. Not installed. `brew install --cask libreoffice` would give
a faithful engine and `soffice --headless --convert-to pdf` would be one line.
Until then this reads the OOXML package we ourselves wrote, which is the one
format this family can be sure it understands.

WHAT IT RENDERS, from the package rather than from the source markdown, so the
PDF shows what the .docx actually contains:
    word/document.xml   paragraphs, styles, tables, images, comment ranges
    word/comments.xml   the evidence cards, printed in the MARGIN beside the
                        text they annotate, which is where Word shows them
    word/media/*        embedded figures
    word/styles.xml     ignored: the page setup below is MISQ's stated one, so
                        a style bug in the package cannot silently pass

    python3 docx2pdf.py <in.docx> [-o out.pdf]

The page setup is MISQ's Author Submission Guidelines, verbatim: Times New Roman
12pt, double-spaced, left-justified, 1-inch margins, letter. That is why this
PDF's page count is comparable to the LaTeX one and textutil's was not.
"""
import argparse
import base64
import html
import os
import re
import subprocess
import zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

CSS = """
@page { size: letter; margin: 1in 1in 1in 1in; }
html, body { margin: 0; padding: 0; }
body { font-family: "Times New Roman", Times, serif; font-size: 12pt;
       line-height: 2.0; text-align: left; }
/* The card FLOATS and stays in flow. It was `position: absolute` in one
   container at top:0, which took all 239 out of flow and stacked every one of
   them at the same y on page 1: a solid unreadable block beside the abstract
   (JL 2026-07-28). Absolute positioning cannot work in a paged medium, because
   the y a card belongs at is not known until the text above it has been laid
   out and broken across pages. A float is laid out BY the flow, so it lands
   beside its own paragraph and paginates for free. */
.page { }
p { margin: 0 0 0 0; text-indent: 0; }
h1, h2, h3 { font-size: 12pt; font-weight: bold; line-height: 2.0;
             margin: 1.5em 0 0 0; }
h1 { text-transform: uppercase; text-align: center; }
h2 { text-align: center; }
h3 { text-align: left; }
/* MIRRORS the .docx: full body width, centred, booktabs rules only (a top and
   a bottom), a real gutter, single-spaced. It used to draw a full cell grid the
   .docx never had, so the two projections disagreed about the same table. */
table { border-collapse: collapse; font-size: 10pt; line-height: 1.15;
        margin: 12pt auto; width: 100%; table-layout: fixed;
        border-top: 0.75pt solid #000; border-bottom: 0.75pt solid #000; }
td, th { padding: 1.5pt 5.4pt; vertical-align: top; }
tr.hdr td, td.b { font-weight: bold; }
img { max-width: 100%; }
.cap { font-size: 10pt; line-height: 1.15; margin: 12pt 0; }
.ref { margin-left: 0.5in; text-indent: -0.5in; line-height: 1.0;
       margin-bottom: 0.15em; }
/* an evidence card. Anchored text is tinted and the card sits in the margin,
   numbered, so the pairing survives a print with no interaction. */
.anchor { background: #eef2ff; }
.mark { vertical-align: super; font-size: 8pt; color: #4338ca;
        font-weight: bold; }
.card { float: right; clear: right; width: 1.9in; margin: 0 0 6pt 0.22in;
        font-size: 7pt; line-height: 1.3;
        font-family: -apple-system, "Helvetica Neue", sans-serif;
        color: #1f2937; background: #f8f9ff;
        border-left: 2pt solid #4338ca; padding: 3pt 4pt;
        /* a card must not be split across a page break, or half an evidence
           record appears with no header saying which sentence it belongs to */
        break-inside: avoid; page-break-inside: avoid; }
.card b { color: #4338ca; }
"""


def text_of(node):
    return "".join(t.text or "" for t in node.iter(W + "t"))


def text_lines(node):
    """text_of, but `w:br` is a line break. Comments carry their structure in
    breaks, so joining only the `w:t` ran a three-reference comment together as
    "…pp. 795-824. key=graziano1997agreeablenessJohn, O. P., …" in this render
    while Word showed it correctly (JL 2026-07-28)."""
    return "".join("\n" if el.tag == W + "br" else (el.text or "")
                   for el in node.iter() if el.tag in (W + "t", W + "br"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.docx)[0] + ".pdf"
    import xml.etree.ElementTree as ET

    z = zipfile.ZipFile(a.docx)
    doc = ET.fromstring(z.read("word/document.xml"))
    comments = {}
    if "word/comments.xml" in z.namelist():
        for c in ET.fromstring(z.read("word/comments.xml")).iter(W + "comment"):
            comments[c.get(W + "id")] = (c.get(W + "author") or "", text_lines(c))
    rels = {}
    if "word/_rels/document.xml.rels" in z.namelist():
        for r in ET.fromstring(z.read("word/_rels/document.xml.rels")):
            rels[r.get("Id")] = r.get("Target")
    media = {n.split("/")[-1]: base64.b64encode(z.read(n)).decode()
             for n in z.namelist() if n.startswith("word/media/")}

    body = doc.find(W + "body")
    html_parts, cards, n_card = [], [], 0

    def render_para(p):
        """-> (paragraph html, [card html, ...]) for THIS paragraph only."""
        nonlocal n_card
        mine = []
        style = ""
        ppr = p.find(W + "pPr")
        if ppr is not None:
            st = ppr.find(W + "pStyle")
            if st is not None:
                style = st.get(W + "val") or ""
        pieces, open_ids = [], []
        for el in p.iter():
            tag = el.tag
            if tag == W + "commentRangeStart":
                open_ids.append(el.get(W + "id"))
                pieces.append('<span class="anchor">')
            elif tag == W + "commentRangeEnd":
                cid = el.get(W + "id")
                if cid in open_ids:
                    open_ids.remove(cid)
                    n_card += 1
                    author, txt = comments.get(cid, ("", ""))
                    pieces.append('</span><span class="mark">%d</span>' % n_card)
                    mine.append('<aside class="card"><b>%d · %s</b><br>%s</aside>'
                                % (n_card, html.escape(author),
                                   html.escape(txt).replace("\n", "<br>")))
            elif tag == W + "t":
                pieces.append(html.escape(el.text or ""))
            elif tag == W + "br":
                pieces.append("<br>")
            elif tag == W + "blip":
                emb = el.get("{http://schemas.openxmlformats.org/officeDocument"
                             "/2006/relationships}embed")
                tgt = (rels.get(emb) or "").split("/")[-1]
                if tgt in media:
                    pieces.append('<img src="data:image/png;base64,%s">' % media[tgt])
        while open_ids:
            pieces.append("</span>")
            open_ids.pop()
        inner = "".join(pieces)
        if not inner.strip():
            return "<p>&nbsp;</p>", mine
        tag = {"Heading1": "h1", "Heading2": "h2", "Heading3": "h3"}.get(style)
        if tag:
            return "<%s>%s</%s>" % (tag, inner, tag), mine
        cls = {"Reference": "ref", "Caption": "cap"}.get(style)
        return "<p%s>%s</p>" % (' class="%s"' % cls if cls else "", inner), mine

    for child in body:
        if child.tag == W + "p":
            para_html, para_cards = render_para(child)
            # cards FIRST: a right float is placed from the line it is declared
            # on, so declaring them before the paragraph puts them level with
            # its first line rather than trailing the one after it.
            html_parts.extend(para_cards)
            html_parts.append(para_html)
        elif child.tag == W + "tbl":
            # the column widths and per-cell alignment the .docx declares, so
            # this render is not a second opinion about the same table
            grid = child.find(W + "tblGrid")
            widths = [int(g.get(W + "w") or 1)
                      for g in (grid.findall(W + "gridCol") if grid is not None else [])]
            cols = ""
            if sum(widths):
                cols = "<colgroup>%s</colgroup>" % "".join(
                    '<col style="width:%.2f%%">' % (100.0 * w / sum(widths))
                    for w in widths)
            rows = []
            for tr in child.findall(W + "tr"):
                cells = []
                for tc in tr.findall(W + "tc"):
                    jc = tc.find(".//" + W + "jc")
                    span = tc.find(".//" + W + "gridSpan")
                    bold = tc.find(".//" + W + "b") is not None
                    cells.append(
                        '<td%s%s%s>%s</td>'
                        % (' colspan="%s"' % span.get(W + "val") if span is not None else "",
                           ' style="text-align:%s"' % jc.get(W + "val")
                           if jc is not None else "",
                           ' class="b"' if bold else "",
                           html.escape(text_of(tc))))
                rows.append("<tr>%s</tr>" % "".join(cells))
            html_parts.append("<table>%s%s</table>" % (cols, "".join(rows)))

    page = ("<!doctype html><meta charset='utf-8'><style>%s</style>"
            "<div class='page'>%s</div>" % (CSS, "".join(html_parts)))
    # the intermediate goes to a dot-file so the delivery folder holds
    # only the .docx and its .pdf
    tmp = os.path.join(os.path.dirname(out) or ".",
                       "." + os.path.basename(os.path.splitext(out)[0])
                       + ".render.html")
    open(tmp, "w", encoding="utf-8").write(page)

    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + os.path.abspath(out),
                    "file://" + os.path.abspath(tmp)],
                   capture_output=True)
    print("✅ %s" % out)
    print("   %d paragraphs · %d tables · %d image(s) · %d evidence card(s) printed"
          % (sum(1 for x in html_parts if x.startswith("<p")),
             sum(1 for x in html_parts if x.startswith("<table")),
             len(media), n_card))
    if os.path.exists(out):
        import shutil
        tool = shutil.which("pdfinfo") or "/opt/homebrew/bin/pdfinfo"
        info = subprocess.run([tool, out], capture_output=True,
                              text=True).stdout if os.path.exists(tool) else ""
        pg = next((l.split()[-1] for l in info.split("\n") if l.startswith("Pages")), "?")
        print("   📄 %s pages, MISQ page setup (TNR 12pt, double-spaced, 1in, letter)" % pg)


if __name__ == "__main__":
    main()
