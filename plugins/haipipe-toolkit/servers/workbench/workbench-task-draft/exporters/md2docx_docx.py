"""The .docx package itself: paragraphs, tables, pictures, comments, and the styles part."""

import re, struct, zipfile
from xml.sax.saxutils import escape
from md2docx_layout import BODY_IN, BODY_TW, DRW, EMU_IN, NUMTOK, OFF, PKG, W, col_widths
from md2docx_inputs import compact_lane
from md2docx_tables import _alignment_columns

# THE COMMENT AUTHOR, and it is a per-run fact rather than a property of the
# format (JL ruling 2026-07-27). The DEFAULT stays `haipipe` because that is
# what QC6 reasoned for: the author field is the partition, so a coauthor can
# see at a glance which comments are machine provenance and which are a person.
# `--author "Junjie Luo"` overrides it when the file is going to a named person
# and the markup should read as theirs. When it is overridden the author no
# longer partitions, so the partition falls back to the LANE-TYPE PREFIX that
# every generated comment already begins with: Value: / Note: / Display: /
# Citation: / Check:. The caller is expected to ASK who the annotator is rather
# than assume; see SKILL.md.
AUTHOR = "haipipe"


def _initials(name):
    """Word shows these in the margin, so "Junjie Luo" -> "JL"."""
    parts = [w for w in re.split(r"[\s_-]+", name.strip()) if w]
    return ("".join(w[0] for w in parts[:3]) or "hp").upper()[:4]


# --------------------------------------------------------------- docx

def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


class Docx:
    def __init__(self):
        self.body, self.comments, self.media = [], [], {}
        self.cid = 0

    # -- runs and paragraphs
    @classmethod
    def run(cls, t, bold=False, style=None):
        """`**bold**` arrives from the board's markdown and Word has no
        markers, so the run splits and the words go BOLD (JL 260816: the twin
        printed the asterisks literally). Only a BALANCED pair converts; an
        odd count (a pair cut in half by a comment-range boundary) passes
        through unchanged, which is exactly what the twin printed before."""
        t = str(t)
        if "**" in t:
            parts = t.split("**")
            if len(parts) % 2 == 1:
                return "".join(cls._run1(seg, bold=bold or (i % 2 == 1),
                                         style=style)
                               for i, seg in enumerate(parts) if seg)
        return cls._run1(t, bold, style)

    @staticmethod
    def _run1(t, bold=False, style=None):
        rpr = ""
        if bold or style:
            rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + \
                  (f'<w:rStyle w:val="{style}"/>' if style else "") + "</w:rPr>"
        # Word collapses a literal newline, so a multi-reference comment ran
        # its entries together: `…pp. 583-599. key=graziano2007… Wilmot, M. P.,`
        # (JL, 2026-07-27). A line break inside a run is an explicit <w:br/>.
        parts = str(t).split("\n")
        body = f'<w:br/>'.join(
            f'<w:t xml:space="preserve">{escape(x)}</w:t>' for x in parts)
        return f'<w:r>{rpr}{body}</w:r>'

    def comment(self, kind, body):
        self.cid += 1
        text = f"{kind}: {compact_lane(kind, body)}"
        self.comments.append(
            f'<w:comment w:id="{self.cid}" w:author="{escape(AUTHOR)}" '
            f'w:initials="{escape(_initials(AUTHOR))}" '
            f'w:date="2026-07-27T09:00:00Z"><w:p><w:pPr><w:pStyle w:val="CommentText"/>'
            f'</w:pPr>{self.run(text)}'
            f'</w:p></w:comment>')
        return self.cid

    def para_with_comments(self, text, lanes, anchor_hint=None):
        """Anchor each lane on the NUMBER it names when that number is in the
        sentence, else on the whole sentence. Anchoring on the digits is the
        thing the LaTeX column cannot do at all."""
        marks = []          # (start, end, cid)
        for lane in lanes:
            # A lane may carry the WINDOW of the sentence it belongs to. Without
            # it, a joined paragraph anchors on the first matching number
            # anywhere in the paragraph, which is a different sentence: `text.
            # index(tok)` cannot know which sentence owed the number.
            kind, body = lane[0], lane[1]
            windowed = len(lane) >= 4
            lo, hi = (lane[2], lane[3]) if windowed else (0, len(text))
            cid = self.comment(kind, body)
            span = None
            lead = body.split("\u00b7")[0]
            for tok in NUMTOK.findall(lead):
                if len(tok) > 1:
                    # a citation's number is its year, and its in-text citation comes after the words it backs, so
                    # the last match is the citation, not an earlier year in the sentence ("in early 2026, ... (Gottfried
                    # et al. 2026)", t01_introduction 261021)
                    i = text.rfind(tok, lo, hi) if kind == "Citation" else text.find(tok, lo, hi)
                    if i >= 0:
                        span = (i, i + len(tok))
                        break
            # FALL BACK TO THE SENTENCE, NEVER TO THE PARAGRAPH. Before joining,
            # "no number found" meant highlight the whole paragraph, and a
            # paragraph WAS one sentence, so it looked right. Joined, the same
            # branch highlighted all eleven sentences of the abstract for one
            # Value lane (JL, 2026-07-27). A lane belongs to the sentence that
            # carried it, and the window says which one; the number is only a
            # refinement inside that.
            if span is None and windowed:
                span = (lo, min(hi, len(text)))
            marks.append((span, cid))

        # AN EVENT WALK, so nothing is ever demoted to the whole paragraph.
        # OOXML permits comment ranges to overlap and to nest, so the two rules
        # that produced paragraph-wide highlights were both unnecessary:
        # demoting an overlap, then demoting a span merely NESTED inside a
        # sentence window (a number inside its own sentence is the common case).
        # Measured on S-Main-all: 69 paragraph-sized ranges, then 19, now 0.
        # The original hazard is still impossible by construction: a start and an
        # end are emitted from the SAME sorted event list, so neither can appear
        # without the other.
        events = {}
        for span, cid in marks:
            a, b = span if span else (0, len(text))
            a, b = max(0, min(a, len(text))), max(0, min(b, len(text)))
            if b <= a:
                a, b = 0, len(text)
            events.setdefault(a, {"open": [], "close": []})["open"].append(cid)
            events.setdefault(b, {"open": [], "close": []})["close"].append(cid)

        xml, cursor = [], 0
        for pos in sorted(events):
            if pos > cursor:
                xml.append(self.run(text[cursor:pos]))
                cursor = pos
            ev = events[pos]
            for c in ev["close"]:
                xml.append(f'<w:commentRangeEnd w:id="{c}"/>')
                xml.append(f'<w:r><w:commentReference w:id="{c}"/></w:r>')
            for c in ev["open"]:
                xml.append(f'<w:commentRangeStart w:id="{c}"/>')
        if cursor < len(text):
            xml.append(self.run(text[cursor:]))

        self.body.append("<w:p>" + "".join(xml) + "</w:p>")

    def para(self, text, style=None, bold=False):
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        self.body.append(f"<w:p>{ppr}{self.run(text, bold=bold)}</w:p>")

    def code(self, text):
        """Emit one kept Markdown fence as a readable monospaced block.

        Board Pages use fenced blocks for compact prompt/specification payloads.
        The LaTeX writer keeps them as verbatim blocks; Word needs the same
        content in a paragraph style rather than silently dropping it.
        """
        self.body.append(
            '<w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr>'
            + self.run(text) + "</w:p>")

    def heading(self, level, text):
        self.para(text, style=f"Heading{level}")

    def title(self, text):
        """Emit a document title independently of the manuscript heading walk."""
        self.para(text, style="Title")

    # -- a real, EDITABLE table. A picture of a table is the wrong answer
    #    because the coauthor cannot fix a typo in it (QC6).
    def table(self, rows, caption=None, align=""):
        """`align` is the unit's own LaTeX column spec (`lccc`), so a numeric
        column is centred here because the author already said it was centred
        there. Without it every cell was left-aligned and auto-width, which is
        why Table 6 printed `+0.0064*** (0.0020)765,701 High`: adjacent columns
        shrank to their content and met with no gutter (JL 2026-07-28)."""
        if caption:
            self.para(caption, style="Caption", bold=True)
        ncol = max((sum(c[2] for c in r) for r in rows), default=1)
        out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
               # FULL BODY WIDTH, FIXED, CENTRED. `w:w="0" type="auto"` let Word
               # autofit, which produced a narrow left-hugging table sitting off
               # to one side of the page (JL 2026-07-28). A journal table spans
               # the text block; `jc center` then makes that symmetric.
               f'<w:tblW w:w="{BODY_TW}" w:type="dxa"/>'
               '<w:jc w:val="center"/>'
               '<w:tblLayout w:type="fixed"/>'
               # a gutter, so neighbouring columns cannot touch
               '<w:tblCellMar>'
               '<w:left w:w="108" w:type="dxa"/><w:right w:w="108" w:type="dxa"/>'
               '<w:top w:w="20" w:type="dxa"/><w:bottom w:w="20" w:type="dxa"/>'
               '</w:tblCellMar>'
               '<w:tblBorders>'
               '<w:top w:val="single" w:sz="6" w:space="0" w:color="auto"/>'
               '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="auto"/>'
               '</w:tblBorders></w:tblPr>']
        out.append("<w:tblGrid>"
                   + "".join(f'<w:gridCol w:w="{w}"/>' for w in col_widths(rows, ncol))
                   + "</w:tblGrid>")
        jc = {"l": "left", "c": "center", "r": "right"}
        spec = _alignment_columns(align)
        # the LEADING bold rows are the header: repeat them when the table breaks
        head = 0
        for r in rows:
            if all(c[1] or not c[0].strip() for c in r):
                head += 1
            else:
                break
        for i, cells in enumerate(rows):
            # a row must not be torn across a page break, which is how Table 5's
            # header stranded at the foot of one page with its body on the next
            out.append('<w:tr><w:trPr><w:cantSplit/>'
                       + ('<w:tblHeader/>' if i < head else "")
                       + "</w:trPr>")
            col = 0
            for text, bold, span in cells:
                a = jc.get(spec[col] if col < len(spec) else "", "left")
                col += span
                tcpr = ("<w:tcPr>"
                        + (f'<w:gridSpan w:val="{span}"/>' if span > 1 else "")
                        + "</w:tcPr>")
                # TableText IS 10pt, AND IT HAS TO BE SAID HERE. The style was
                # declared and never applied, so Word rendered cells at the
                # document's 12pt while `col_widths` and docx2pdf both sized
                # them at 10pt: every column was ~20% too narrow for its own
                # content and "Accountability" broke as "Accountabil / ity"
                # (JL 2026-07-28). It also carries the single spacing, which
                # cells otherwise inherit as the document's double.
                ppr = ('<w:pPr><w:pStyle w:val="TableText"/>'
                       '<w:spacing w:before="20" w:after="20" w:line="240" '
                       f'w:lineRule="auto"/><w:jc w:val="{a}"/></w:pPr>')
                out.append(f"<w:tc>{tcpr}<w:p>{ppr}{self.run(text, bold=bold)}</w:p></w:tc>")
            out.append("</w:tr>")
        out.append("</w:tbl>")
        self.body.append("".join(out))
        self.body.append("<w:p/>")

    def image(self, path, caption=None):
        rid = f"rIdImg{len(self.media) + 1}"
        name = f"media/image{len(self.media) + 1}.png"
        self.media[name] = (rid, path)
        size = png_size(path)
        if size:
            w, h = size
            cx = int(BODY_IN * EMU_IN)
            cy = int(cx * h / w)
        else:
            cx, cy = int(BODY_IN * EMU_IN), int(3.5 * EMU_IN)
        did = len(self.media)
        self.body.append(
            # keepNext: the caption sits BELOW the image, so without it Word may
            # break between them and print a figure with no caption
            f'<w:p><w:pPr><w:keepNext/><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline xmlns:wp="{DRW}/wordprocessingDrawing">'
            f'<wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:docPr id="{did}" name="Picture {did}"/>'
            f'<a:graphic xmlns:a="{DRW}/main">'
            f'<a:graphicData uri="{DRW}/picture">'
            f'<pic:pic xmlns:pic="{DRW}/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{did}" name="image{did}.png"/>'
            f'<pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip xmlns:r="{OFF}" r:embed="{rid}"/>'
            f'<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
            f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            f'</pic:pic></a:graphicData></a:graphic></wp:inline>'
            f'</w:drawing></w:r></w:p>')
        if caption:
            self.para(caption, style="Caption", bold=True)

    # -- package
    def save(self, out):
        rels = [f'<Relationship Id="rIdC" Type="{OFF}/comments" Target="comments.xml"/>',
                f'<Relationship Id="rIdS" Type="{OFF}/styles" Target="styles.xml"/>']
        for name, (rid, _) in self.media.items():
            rels.append(f'<Relationship Id="{rid}" Type="{OFF}/image" Target="{name}"/>')

        ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
              '<Default Extension="xml" ContentType="application/xml"/>',
              '<Default Extension="png" ContentType="image/png"/>',
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>',
              '<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>',
              '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>',
              '</Types>']

        doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
               f'<w:document xmlns:w="{W}" xmlns:r="{OFF}"><w:body>'
               + "".join(self.body) +
               '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
               '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
               '</w:sectPr></w:body></w:document>')

        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", "\n".join(ct))
            z.writestr("_rels/.rels",
                       f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       f'<Relationships xmlns="{PKG}">'
                       f'<Relationship Id="rId1" Type="{OFF}/officeDocument" Target="word/document.xml"/>'
                       f'</Relationships>')
            z.writestr("word/document.xml", doc)
            z.writestr("word/_rels/document.xml.rels",
                       f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       f'<Relationships xmlns="{PKG}">{"".join(rels)}</Relationships>')
            z.writestr("word/comments.xml",
                       f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       f'<w:comments xmlns:w="{W}">{"".join(self.comments)}</w:comments>')
            z.writestr("word/styles.xml", STYLES)
            for name, (_, path) in self.media.items():
                z.write(path, "word/" + name)


STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W}">
<!-- Every value below is STATED by MISQ's Author Submission Guidelines
     (venue/playbook-utd-is/MISQ/instructions/20260727.md), not chosen here.
       body        Times New Roman 12pt, DOUBLE-spaced, LEFT-justified, 1in margins
       headings    1 MAJOR HEAD  bold, ALL CAPS, centered
                   1.1 Subhead   bold, title case, centered
                   1.1.1         bold, title case, flush left
       references  Times New Roman 12pt, SINGLE-spaced, left hanging indent
       tables      may use a smaller font and may be single-spaced
     w:sz is HALF-points, so 24 = 12pt. w:line is twentieths of a point on an
     `auto` rule, so 480 = double and 240 = single. -->
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>
<w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:pPr><w:outlineLvl w:val="0"/><w:spacing w:before="480" w:after="0" w:line="480" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:caps/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>
<w:pPr><w:keepNext/><w:spacing w:before="0" w:after="360" w:line="300" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:pPr><w:outlineLvl w:val="1"/><w:spacing w:before="480" w:after="0" w:line="480" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>
<w:pPr><w:outlineLvl w:val="2"/><w:spacing w:before="480" w:after="0" w:line="480" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Reference"><w:name w:val="Reference"/>
<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:left="720" w:hanging="720"/><w:jc w:val="left"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/>
<!-- before/after: a caption with w:after="0" touched the paragraph under it, so
     the figure caption and the body text that followed read as one block
     (JL 2026-07-28). keepNext holds a table caption to its table. -->
<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="240" w:line="240" w:lineRule="auto"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/></w:rPr></w:style>
<!-- basedOn + rFonts are NOT decoration: a style with neither inherits from
     docDefaults, which this package does not write, so Word would have set the
     table in its own default face while the body stayed Times New Roman.
     MISQ allows a table a smaller font, and 20 half-points is 10pt. -->
<w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/>
<w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="CommentText"><w:name w:val="annotation text"/>
<w:rPr><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/>
<w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/>
<w:shd w:val="clear" w:color="auto" w:fill="F4F4F5"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/></w:style>
</w:styles>'''
