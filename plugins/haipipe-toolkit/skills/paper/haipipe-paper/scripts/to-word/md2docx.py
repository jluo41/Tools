#!/usr/bin/env python3
"""md2docx.py -- one stage page's ## Content becomes a .docx whose APPARATUS
rides in anchored Word comments.

QC6's ruling, executed. The carrier is a native Word comment with
`w:author="haipipe"`, which is what keeps machine provenance separable from a
coauthor's own markup and is what makes the backport ruling mechanical.

Standard library only, on purpose: pandoc cannot WRITE Word comments at all,
so the obvious tool cannot carry this exporter's central feature.

Nothing here formats a citation or recomputes a number. Every resolved thing
is read from a file the family already generates:
    .board-refs.bbl                 the in-text label AND the reference list,
                                    produced by the paper's own .bst
    displays/<unit>/float.tex       the \\label and the unit's kind
    displays/<unit>/assets/         table-body.tex or figure.png

Usage:  md2docx.py <S-page.md> [-o out.docx] [--paper-root DIR]
"""
import argparse, os, re, struct, sys, zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
OFF = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
DRW = "http://schemas.openxmlformats.org/drawingml/2006"
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
LANES = ("Value:", "Note:", "Display:", "Citation:", "Check:")   # the fallback partition
EMU_IN = 914400


def _initials(name):
    """Word shows these in the margin, so "Junjie Luo" -> "JL"."""
    parts = [w for w in re.split(r"[\s_-]+", name.strip()) if w]
    return ("".join(w[0] for w in parts[:3]) or "hp").upper()[:4]
BODY_IN = 6.0               # usable text width
BODY_TW = 9360              # the same width in twentieths of a point, for tables


# Approximate advance widths in TWIPS for 10pt Times New Roman. Character COUNT
# was the first proxy and it is too coarse in the direction that matters: a
# results column is digits, which are half again as wide as lowercase, so
# "+12.90*** (3.68)" needs more room than the 16 characters of a row label
# suggest and was landing 0.02in inside its column.
_TW = {" ": 50, ".": 50, ",": 50, ";": 50, ":": 50, "(": 67, ")": 67,
       "*": 70, "-": 67, "–": 100, "+": 113, "=": 113, "%": 167}
_TW.update({c: 100 for c in "0123456789"})


def text_tw(s):
    return sum(_TW.get(c, 132 if c.isupper() else 89) for c in s)


def col_widths(rows, ncol, total=BODY_TW, pad=216):
    """Split `total` across `ncol` columns, `pad` covering two cell margins.

    Two numbers per column, and the distinction is the whole point:

        WANT   its widest whole cell, one line, no wrapping
        FLOOR  its widest UNBREAKABLE token

    A column may wrap between words: Table 4's middle column is a sentence of
    definition and is supposed to. A column may never break INSIDE a word, which
    is what "Agreeable / ness" and "1,204,6 / 07" were (JL 2026-07-28). So the
    floor is satisfied first and only the slack is shared out toward want.
    Word breaks after a hyphen and a slash, so those end a token here too."""
    want, floor = [1] * ncol, [1] * ncol
    for cells in rows:
        col = 0
        for text, _bold, span in cells:
            if span == 1 and col < ncol:               # a span tells us nothing
                want[col] = max(want[col], text_tw(text) + pad)  # about one column
                for tok in re.split(r"[\s/]|(?<=-)", text):
                    floor[col] = max(floor[col], text_tw(tok) + pad)
            col += span
    if sum(floor) >= total:          # cannot be honoured; scale it down evenly
        w = [max(1, int(x * total / sum(floor))) for x in floor]
    else:
        slack = total - sum(floor)
        head = [max(0, want[i] - floor[i]) for i in range(ncol)]
        w = [floor[i] + (int(slack * head[i] / sum(head)) if sum(head) else
                         slack // ncol) for i in range(ncol)]
    w[w.index(max(w))] += total - sum(w)               # rounding to the widest
    return w

# lanes that are EVIDENCE and become comments; see QC0 on typed lanes
# THE EVIDENCE LANES, and there are exactly three. This is not our list: it is
# the board's own, at haipipe-board/src/body.py:288, "Typed evidence lanes
# (`> Citation:`, `> Value:`, `> Display:`)". Each one answers "what backs this
# sentence" and resolves against a file: the .bib, a run, a display unit.
EVIDENCE_LANES = ("Value", "Citation", "Display")
# NOT evidence, and they used to be exported as though they were (JL 260727:
# "for the sentences, we might have multiple comments, don't render them to the
# word, only the evidence card"). A `Note` is a PENDING candidate edit, so it is
# a review artifact about prose that has not been accepted. A `Check` is a gate
# REPORT about the section. Neither backs the sentence, and a coauthor reading
# the manuscript should not be handed our unresolved internal queue. They stay
# on the board, where they belong; they are counted on the way out, never
# silently dropped.
WORKING_LANES = ("Note", "Check", "Citation")
# `Citation` is in that list and it looks surprising, so: the CITATION COMMENT IS
# GENERATED, from `.board-refs.bbl`, and carries the reference plus the key. That
# is the evidence card. A hand-written `> Citation:` lane carries something else
# entirely: the `.bib` line number, where the key sits in the tex, a hit count, a
# de-duplication history. All true, all useful on the board, and none of it is
# what a coauthor checks. Merged in, one comment ran to 605 characters for a
# reference of 240 (JL 260727: "Too long, I think we only need: Citation: <the
# reference> key=<the key>"). So the generated half goes to Word and the
# hand-written half stays on the board.
# lanes that are people talking; dropped, same as the LaTeX column
DISCUSSION_LANES = ("JL", "CC", "USER", "Also")
# Content divisions that are the stage's own bookkeeping, not manuscript
# A MANUSCRIPT HEADING IS NUMBERED. That is MISQ's own contract: `1 MAJOR HEAD`,
# `1.1 First Subhead`, `1.1.1 Second Subhead`. So rather than grow a list of
# scaffolding names forever, the test is inverted: a `###` under ## Content is a
# manuscript heading only if it opens with a number, or is one of the few
# unnumbered divisions a manuscript really has. Everything else is working
# structure. Two had already slipped through a name-based list and printed as
# MAJOR HEADS in the export: "(Closing paragraph -- no subsection title)" in §2
# and "Display drafts (markdown-first; NOW FILED as DR requests …)" in §5
# (JL 260727).
SKIP_DIVISIONS = ("Stage Record", "Stage Contract")
UNNUMBERED_OK = ("Abstract", "References", "Acknowledgements", "Appendix")


def is_manuscript_heading(title):
    return bool(re.match(r"^\d+(?:\.\d+)*\s", title)) or \
        any(title.startswith(x) for x in UNNUMBERED_OK)

NUMTOK = re.compile(r"[+-]?\d[\d,]*(?:\.\d+)?%?")


# --------------------------------------------------------------- inputs

class Bbl:
    """`\\bibitem[{Author and Author(2024)}]{key}` -- the bracket IS the
    natbib in-text label, set by the manuscript's own .bst. So the in-text
    form is READ, never formatted here."""

    # The braces around the label are the .bst's choice, not natbib's law:
    # misq.bst emits `[{Author(2024)}]`, plainnat emits `[Author(2024)...]`
    # bare. Both are read; demanding the braces made every plainnat .bbl
    # parse to nothing and cites print bare keys (found via the board's
    # page-owned bibex store, 2026-08-15).
    ENTRY = re.compile(r"\\bibitem\[\{?(.*?)\}?\]\{([^}]+)\}(.*?)(?=\\bibitem\[|\\end\{thebibliography\})",
                       re.S)

    def __init__(self, path):
        self.intext, self.body = {}, {}
        if not path or not os.path.exists(path):
            return
        raw = open(path, encoding="utf-8", errors="replace").read()
        for label, key, body in self.ENTRY.findall(raw):
            self.intext[key] = self._intext(label)
            self.body[key] = detex(body)

    @staticmethod
    def _intext(label):
        """natbib packs BOTH forms into one label: `SHORT(YEAR)FULL`, e.g.
        `Wang et~al.(2022)Wang, Luo, Dugas, Gao, Agarwal, and Werner`. Only
        the part up to the year is the in-text call; the trailing full author
        list belongs to the reference entry. Taking the whole label produced
        `(Wang et al.(2022)Wang, Luo, Dugas, ...)` in the first export run."""
        s = detex(label)
        m = re.match(r"(.*?)\s*\((\d{4}[a-z]?)\)", s)
        if m:
            return f"{m.group(1).strip()} {m.group(2)}"
        return s.strip()


class Displays:
    """Every display unit on disk, by \\label. Kind comes from the unit's own
    float.tex, per QC3: the board does not guess table from figure."""

    def __init__(self, paper_root, extra_root=None):
        self.by_label, self.by_unit = {}, {}
        base = None
        for cand in ("displays", "0-displays"):
            p = os.path.join(paper_root, cand)
            if os.path.isdir(p):
                base = p
                break
        if base:
            self._scan(base)
        # A SECOND unit root, for callers whose units live outside the paper
        # convention: a board page's plugin folder is `<page>/display/` (the
        # page-as-small-paper contract, QPf5), and without this hook every
        # projection of such a page shipped its evidence citations as plain
        # text (JL 260816: "both word and latex didn't include the display?").
        if extra_root and os.path.isdir(extra_root):
            self._scan(extra_root)

    def _scan(self, base):
        for unit in sorted(os.listdir(base)):
            f = os.path.join(base, unit, "float.tex")
            if not os.path.exists(f):
                continue
            tex = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"\\begin\{(table|figure)", tex)
            lab = re.search(r"\\label\{([^}]+)\}", tex)
            assets = os.path.join(base, unit, "assets")
            # THE UNIT'S OWN CAPTION. Without it the .docx printed
            # "Figure 1. display01a-hero-concept", a folder name, where the
            # published caption belongs (JL 2026-07-28). It is read here rather
            # than composed, for the same reason the citation is read from the
            # .bbl: the manuscript's caption is authored in the unit and this
            # projection must not invent a second one.
            cap = ""
            i = tex.find("\\caption{")
            if i >= 0:
                k, depth = i + 9, 1
                while k < len(tex) and depth:
                    depth += (tex[k] == "{") - (tex[k] == "}")
                    k += 1
                cap = tex[i + 9:k - 1].strip()
            rec = {
                "unit": unit,
                # the RAW tex. detex is deferred to emit time so the Resolver can
                # turn a \ref inside the caption into its number first.
                "caption": cap,
                "kind": m.group(1) if m else "unknown",
                "label": lab.group(1) if lab else None,
                "body": os.path.join(assets, "table-body.tex"),
                "pdf": next((os.path.join(assets, n) for n in ("figure.pdf",)
                             if os.path.exists(os.path.join(assets, n))), None),
                "image": next((os.path.join(assets, n) for n in ("figure.png",)
                               if os.path.exists(os.path.join(assets, n))), None),
            }
            self.by_unit[unit] = rec
            if rec["label"]:
                self.by_label[rec["label"]] = rec


def _braced(s, cmd, wrap=("", "")):
    """Replace `\\cmd{...}` using BALANCED braces, not a non-greedy match.

    A non-greedy `\\enquote\{(.*?)\}` stops at the first `}` it meets, and a
    .bib protects capitals as `{U}nited {S}tates`, so the very first title with
    a protected capital came out as `"…in the U"nited States` and shipped a
    mangled reference to the reader. Found 2026-07-27 on `guy2017vital`.
    """
    out, i, n = [], 0, len(cmd)
    while i < len(s):
        j = s.find(cmd, i)
        if j < 0:
            out.append(s[i:])
            break
        out.append(s[i:j])
        k, depth = j + n, 0
        while k < len(s):
            if s[k] == "{":
                depth += 1
            elif s[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        if depth != 0:                      # unbalanced: leave it alone
            out.append(s[j:j + n])
            i = j + n
            continue
        out.append(wrap[0] + s[j + n + 1:k] + wrap[1])
        i = k + 1
    return "".join(out)



DIFF = re.compile(r"~~(.*?)~~\s*(?:\*\*(.*?)\*\*)?|\*\*(.*?)\*\*")


def compact_lane(kind, body):
    """A comment carries the CHANGE, never a restatement of the sentence.

    JL, 2026-07-27: "Just add the comments for the evidence card, don't add the
    whole sentences." A `> Note:` lane holds a complete candidate sentence with
    `~~removed~~ **inserted**` inside it, which is right on the Board, where the
    original sits directly above it for comparison. In Word the sentence is
    already there in the body, so restating it put a full paragraph in the margin
    and buried the one or two words that actually changed.

    So a Note is reduced to its edits: `across -> from`. Everything else is left
    alone, because a Value or Display lane is already the evidence card and
    nothing in it is a restatement.
    """
    if kind != "Note":
        return body
    tail = ""
    for sep in (" \u00b7 GPT-5", " \u00b7 Claude", " \u00b7 haipipe"):
        if sep in body:
            body, tail = body.split(sep, 1)[0], sep + body.split(sep, 1)[1]
            break
    edits = []
    for removed, inserted, added in DIFF.findall(body):
        if removed and inserted:
            edits.append(f"{removed.strip()} \u2192 {inserted.strip()}")
        elif removed:
            edits.append(f"{removed.strip()} \u2192 (removed)")
        elif added:
            edits.append(f"(added) {added.strip()}")
    if not edits:
        return body.strip() + tail          # a plain note, not a diff: keep it
    return " \u00b7 ".join(edits) + tail



KEYEQ = re.compile(r"key=\s*([A-Za-z0-9_:.-]+)")


def merge_lanes(auto, hand):
    """One citation, ONE comment (JL 260727).

    Two sources produce a Citation lane and they are both legitimate. The
    exporter generates one from the `\\citep{}` marker, carrying the reference
    as `.board-refs.bbl` renders it. The S page may ALSO carry a hand-written
    `> Citation:` lane, carrying what only a person knows: the `.bib` line, where
    the key is placed in the tex, the hit count, a de-duplication history. Left
    alone the reader got two bubbles for `gray2021clinical` and had to work out
    that they were the same source.

    So they merge on the KEY: the reference first, because that is what a reader
    checks, then the lane's own note. A hand lane naming no key, or naming one
    the prose does not cite, is kept as its own comment rather than dropped.
    """
    by_key = {}
    for i, (kind, body) in enumerate(auto):
        if kind == "Citation":
            for k in KEYEQ.findall(body):
                by_key[k] = i
    out, used = list(auto), set()
    for kind, body in hand:
        keys = KEYEQ.findall(body) if kind == "Citation" else []
        hit = next((by_key[k] for k in keys if k in by_key), None)
        if hit is None:
            out.append((kind, body))
        else:
            used.add(hit)
            k0, b0 = out[hit]
            out[hit] = (k0, b0 + "\n" + body.strip())
    return out



DPI = 200          # print-acceptable without making a .docx enormous


def rasterize(pdf, cache_dir, report):
    """A `figure.pdf` becomes a PNG so Word can embed it.

    Word cannot place a PDF as an image, and a display unit legitimately ships
    only `assets/figure.pdf` (JL 260727: display01a and display01b both did). So
    something has to rasterize, and the question is WHO.

    Not the display layer, because this is not a new approved asset; not into
    `displays/`, because an exporter writing into the deliverable is the boundary
    QD1 draws. So it rasterizes into its OWN build area under `3-dist/`, caches
    by mtime, and the unit on disk is untouched. If no converter is present the
    figure is reported missing exactly as before, rather than failing the run.
    """
    import shutil, subprocess
    tool = shutil.which("pdftoppm")
    if not tool:
        report.append(("no-converter",
                       "pdftoppm is not installed, so a figure.pdf cannot be "
                       "rasterized for Word. brew install poppler"))
        return None
    os.makedirs(cache_dir, exist_ok=True)
    out = os.path.join(cache_dir, os.path.basename(os.path.dirname(
        os.path.dirname(pdf))) + ".png")
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(pdf):
        return out                                   # cached and current
    r = subprocess.run([tool, "-r", str(DPI), "-png", "-singlefile",
                        pdf, out[:-4]], capture_output=True, text=True)
    if not os.path.exists(out):
        report.append(("rasterize-failed",
                       f"{os.path.basename(pdf)}: {(r.stderr or '').strip()[:120]}"))
        return None
    report.append(("figure-rasterized",
                   f"{os.path.basename(os.path.dirname(os.path.dirname(pdf)))}: "
                   f"figure.pdf -> PNG at {DPI} dpi, cached under 3-dist/. The unit "
                   f"ships no figure.png; Word cannot embed a PDF."))
    return out


SUPER = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def detex(s):
    """Enough de-TeX for a coauthor to read. Not a TeX engine."""
    s = _braced(s, "\\enquote", ('"', '"'))
    s = re.sub(r"\\natexlab\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\{\\(?:it|em|bf|tt)\s*(.*?)\\/?\}", r"\1", s, flags=re.S)
    for c in ("\\textit", "\\textbf", "\\emph", "\\texttt"):
        s = _braced(s, c)
    s = re.sub(r"\\url\{(.*?)\}", r"\1", s, flags=re.S)
    # inline math, before the catch-all command strip. `$\times$` used to lose
    # \times to the strip and leave the bare `$$`, which shipped as
    # "a person$$ situation perspective" (JL, 2026-07-27).
    # Replace longer command names first.  Otherwise ``\\geq`` is partially
    # consumed by ``\\ge`` and ships as the visible residue ``≥q``.
    for cmd, ch in (("times", "\u00d7"), ("leq", "\u2264"), ("geq", "\u2265"),
                    ("le", "\u2264"), ("ge", "\u2265"),
                    ("pm", "\u00b1"), ("approx", "\u2248"), ("alpha", "\u03b1"),
                    ("beta", "\u03b2"), ("kappa", "\u03ba"), ("mu", "\u03bc")):
        s = s.replace("\\" + cmd + " ", ch).replace("\\" + cmd, ch)
    s = re.sub(r"\$([^$]*)\$", r"\1", s)          # drop the math delimiters
    # SUPERSCRIPTS. `$^{***}$` lost its delimiters above and then its braces
    # below, so every significance star in every table cell shipped as the
    # literal `9.3438^***` (JL 2026-07-28). Word can superscript a run, but this
    # function returns plain text, and bare `***` is the reading convention in a
    # results table anyway. Digits become real superscript characters.
    s = re.sub(r"\^\{?(\*+)\}?", r"\1", s)
    s = re.sub(r"\^\{?([0-9])\}?", lambda m: SUPER[int(m.group(1))], s)
    s = s.replace("~", " ").replace("--", "\u2013").replace("\\&", "&")
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()


# --------------------------------------------------------------- page parse

def parse_page(path, keep_fences=False):
    """Return the blocks of `## Content`, dropping what QC5's read-and-drop
    table drops. A `>` lane binds to the paragraph ABOVE it, which is QC0's
    adjacency law.

    `keep_fences` is the BOARD exporter's switch (JL 260815: a board page's
    figure-only division exported as an empty section). A paper still drops
    sketches, because its figures are display units; a board page's sketch IS
    the content, so the board asks for `("fence", text)` blocks instead."""
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
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
    if page_title and not own_h1:
        blocks.append(("h", 1, page_title))
    in_fence, fenced = False, 0
    for raw in lines[start + 1:end]:
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
            if not skipping and not is_manuscript_heading(title):
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
                blocks.append(("h", lvl, title))
            prev_was_para = False
            continue
        if skipping:
            continue
        if s.startswith("#### "):
            # the paragraph job line is SCAFFOLDING, not manuscript. But the
            # heading itself IS the paragraph boundary, and nothing downstream
            # could see that before, so joining had nowhere to break.
            blocks.append(("pbreak",))
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
            if blocks and blocks[-1][0] == "p":
                blocks[-1][3].append((kind, body))
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


# --------------------------------------------------------------- inline

class Inline:
    """Resolves the markers inside one sentence and returns (runs, comments).

    A run is (text, bold). A comment is (anchor_text_or_None, kind, body)."""

    CITE = re.compile(r"\\cite[a-z]*\{([^}]*)\}")
    REF = re.compile(r"\\ref\{([^}]*)\}")
    BRACKET_REF = re.compile(r"\b(Table|Figure)\s+\[([^\]]+)\]")
    QREF = re.compile(r"\s*\[Q-[A-Za-z0-9]+-\d+\]")
    VALHOLE = re.compile(r"\{VAL:\?[^}]*\}")

    def __init__(self, bbl, displays, numbering, report):
        self.bbl, self.displays = bbl, displays
        self.num = numbering          # {'table': n, 'figure': n, label -> label}
        self.report = report

    def _cite(self, m):
        keys = [k.strip() for k in m.group(1).split(",") if k.strip()]
        if keys == ["TOADD"]:
            self.report.append(("owed-citation", "\\cite{TOADD} shipped to the reader"))
            return "[CITATION OWED]"
        labels = []
        for k in keys:
            lab = self.bbl.intext.get(k)
            if lab:
                labels.append(lab)
                self.cited.add(k)
            else:
                labels.append(k)
                self.report.append(("unresolved-key", f"{k} is not in .board-refs.bbl"))
        # THE COMMENT CARRIES THE REFERENCE, not just the key (JL 2026-07-27).
        # A coauthor reading a .docx cannot grep a .bib, so a bare `key=` names
        # something they have no way to look up. The reference text comes from
        # `.board-refs.bbl`, which `refs.py` produced by running the PAPER'S OWN
        # .bst, so the format here is whatever the manuscript will actually
        # print. That is the point: nothing is formatted twice, so nothing can
        # disagree. Same principle the in-text label already used.
        lines = []
        for k in keys:
            ref = self.bbl.body.get(k, "").strip()
            lines.append(f"{ref}\n    key={k}" if ref
                         else f"key={k} \u00b7 NO ENTRY in .board-refs.bbl, so no "
                              f"reference can be shown; regenerate it with refs.py")
        # A BLANK LINE BETWEEN REFERENCES. One `\citep{a,b,c}` is one comment,
        # and joining on a single newline ran three references together into a
        # wall the reader had to re-parse to see where one ended (JL 2026-07-28).
        self.pending.append(("Citation", "\n\n".join(lines)))
        return "(" + "; ".join(labels) + ")"

    def _ref(self, m):
        label = m.group(1)
        rec = self.displays.by_label.get(label)
        if not rec:
            self.report.append(("broken-ref", f"\\ref{{{label}}} matches no display unit \\label"))
            self.pending.append(("Display", f"\\ref{{{label}}} resolves to no unit; it compiles to ??"))
            return f"[{label}]"
        n = self.num.assign(rec)
        self.pending.append(("Display", f"{rec['unit']} · kind={rec['kind']} · label={label}"))
        # THE AUTHOR WRITES THE WORD, \ref SUPPLIES THE NUMBER. That is LaTeX's
        # own division of labour, so prose reads `Table~\ref{tab:x}` and emitting
        # the kind again gave "Table~Table 5" on every cross-reference
        # (JL 2026-07-28). Only name the kind when the prose did not.
        if re.search(r"(?:table|figure)s?[~\s]*$", m.string[:m.start()], re.I):
            return str(n)
        return f"{rec['kind'].capitalize()} {n}"

    def _bracket_ref(self, m):
        kind, slug = m.group(1), m.group(2)
        self.report.append(("placeholder-ref",
                            f"{kind} [{slug}] is a placeholder, not a \\ref{{}}; "
                            f"it names no display unit"))
        self.pending.append(("Display", f"placeholder reference {kind} [{slug}], unresolved"))
        return f"{kind} [{slug}]"

    def render(self, text):
        self.pending, self.cited = [], getattr(self, "cited", set())
        t = text
        for hole in self.VALHOLE.findall(t):
            self.report.append(("owed-value", f"{hole} shipped to the reader"))
        t = self.CITE.sub(self._cite, t)
        t = self.REF.sub(self._ref, t)
        t = self.BRACKET_REF.sub(self._bracket_ref, t)
        t = self.QREF.sub("", t)                 # the bracket is bookkeeping
        # Inline code is operational text, not typography. Stash it before the
        # prose smart-dash pass so CLI flags such as `--execute` remain exactly
        # executable in the DOCX and its PDF twin.
        code_spans = []

        def _stash_code(m):
            code_spans.append(m.group(1))
            return f"\ue000CODE{len(code_spans) - 1}\ue001"

        t = re.sub(r"`([^`]*)`", _stash_code, t)
        t = t.replace("--", "\u2013")
        for i, code in enumerate(code_spans):
            t = t.replace(f"\ue000CODE{i}\ue001", code)
        # `~` is a non-breaking space, and body prose is not detex'd, so it was
        # printing as a literal tilde inside every "Table~5" (JL 2026-07-28).
        t = t.replace("~", "\u00a0")
        return t, self.pending

    def caption(self, tex):
        """A caption is prose too, so its \\ref{} must resolve. Table 6's read
        "the per-cohort estimates behind Figure fig:discretion-gradient", the
        bare label, because detex strips the command and leaves its argument
        (JL 2026-07-28). Numbering is SHARED with the body, so a caption that
        forward-references a later float still names the number the body will
        give it."""
        self.pending = []            # a caption raises no evidence card
        out = self.REF.sub(self._ref, tex)
        self.pending = []
        return detex(out)


class Numbering:
    """Word has no floats, so a number is order of appearance and the
    exporter owns it because it walks the sections in order."""

    def __init__(self):
        self.counts, self.given = {"table": 0, "figure": 0}, {}

    def assign(self, rec):
        u = rec["unit"]
        if u not in self.given:
            self.counts[rec["kind"]] = self.counts.get(rec["kind"], 0) + 1
            self.given[u] = self.counts[rec["kind"]]
        return self.given[u]


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
                    i = text.find(tok, lo, hi)
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
        spec = [c for c in align if c in jc]
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
                # content and "Agreeableness" broke as "Agreeable / ness"
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
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/></w:style>
</w:styles>'''


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
    for line in raw.split(r"\\"):
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


# --------------------------------------------------------------- driver

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="+",
                    help="one S page, or SEVERAL in reader order for a combined "
                         "manuscript. Several is not a convenience: float "
                         "numbering, the reference list and heading numbers are "
                         "DOCUMENT-level facts, so only one walk over all pages "
                         "in order can get them right (QC6's section-only rows).")
    ap.add_argument("-o", "--out")
    ap.add_argument("--paper-root")
    ap.add_argument("--document-title",
                    help="optional full-document title emitted before Content; "
                         "Board passes the page's canonical H1")
    ap.add_argument("--author", default=AUTHOR,
                    help='comment author. Default "haipipe" keeps QC6\'s '
                         'partition in the author field; pass a person\'s name '
                         'when the markup should read as theirs. ASK first.')
    ap.add_argument("--join-paragraphs", action="store_true",
                    help="join the sentences of each #### block into ONE Word "
                         "paragraph. The .md is one sentence per line, which is "
                         "right for review and wrong for a manuscript: unjoined, "
                         "a 6-sentence paragraph becomes 6 double-spaced Word "
                         "paragraphs, reads as a list, and inflates the page "
                         "count. Use it for the COMBINED document; leave it off "
                         "for per-section review files, where a sentence per "
                         "paragraph is the point.")
    ap.add_argument("--no-displays", action="store_true",
                    help="skip embedding tables and figures")
    ap.add_argument("--display-root",
                    help="an EXTRA folder of display units (each subfolder a "
                         "unit with float.tex), scanned beside the paper's "
                         "displays/: a board page's <page>/display/ plugin")
    ap.add_argument("--lanes", default="Citation",
                    help="which EVIDENCE lanes become comments, comma-separated: "
                         "Citation, Value, Display. Default Citation only. All "
                         "three are evidence and all three are true, but five "
                         "comments landed on one sentence of §1 and three of them "
                         "were Display audits several hundred characters long "
                         "(JL 2026-07-28): a display's state is a BOARD concern, "
                         "and the coauthor reading the .docx is checking the "
                         "sentence. Pass Citation,Value,Display to get them back.")
    a = ap.parse_args()
    lanes = tuple(x.strip() for x in a.lanes.split(",") if x.strip())
    bad = [x for x in lanes if x not in EVIDENCE_LANES]
    if bad:
        raise SystemExit("--lanes: %s is not an evidence lane; pick from %s"
                         % (", ".join(bad), ", ".join(EVIDENCE_LANES)))
    globals()['AUTHOR'] = a.author

    pages = [os.path.abspath(x) for x in a.page]
    root = os.path.abspath(a.paper_root) if a.paper_root else \
        os.path.dirname(os.path.dirname(os.path.dirname(pages[0])))
    stem = (os.path.splitext(os.path.basename(pages[0]))[0] if len(pages) == 1
            else "combined")
    out = a.out or os.path.join(root, "3-dist", "word", stem + ".docx")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    report, num = [], Numbering()
    # STALENESS IS COMPUTED, NEVER DECLARED (QC3's law, applied here).
    # Compared MTIMES first and that was wrong: an editor save with no content
    # change makes the .bib newer than the cache, so the warning fired forever
    # (measured 2026-07-27, .bib touched 7s after a fresh regeneration). What
    # actually matters is whether the cache RENDERS every key the .bib DECLARES,
    # which is exact, cheap, and immune to a touch. It also names the keys.
    bbl_path = os.path.join(root, ".board-refs.bbl")
    bib = next((os.path.join(root, f) for f in sorted(os.listdir(root))
                if f.endswith(".bib")), None)
    if bib and os.path.exists(bbl_path):
        declared = set(re.findall(r"^@\w+\s*\{\s*([^,\s]+)\s*,",
                                 open(bib, encoding="utf-8", errors="replace").read(), re.M))
        rendered = set(re.findall(r"\\bibitem\[[^\]]*\]\{([^}]+)\}",
                                 open(bbl_path, encoding="utf-8", errors="replace").read()))
        gap = sorted(declared - rendered)
        if gap:
            report.append((
                "stale-bibliography",
                f".board-refs.bbl renders {len(rendered)} of the .bib's "
                f"{len(declared)} keys. {len(gap)} declared key(s) are absent, so "
                f"citing any of them prints a bare key: "
                f"{', '.join(gap[:6])}{' …' if len(gap) > 6 else ''}. "
                f"Regenerate: python3 <haipipe-board>/refs.py <paper-root>"))
    bbl = Bbl(bbl_path)
    disp = Displays(root, extra_root=a.display_root)
    inline = Inline(bbl, disp, num, report)
    d = Docx()
    if a.document_title:
        d.title(a.document_title)

    placed, npara, skipped, held = set(), 0, {}, {}
    for page in pages:
        blocks, nfenced = parse_page(page)
        if nfenced:
            report.append(("fenced-sketch-skipped",
                           f"{os.path.basename(page)}: {nfenced} ``` block(s) in "
                           f"## Content are ASCII sketches, not prose, and were "
                           f"NOT exported. Each is usually a display unit that "
                           f"has not been built."))
        buf = []          # [(rendered_sentence, lanes)] awaiting a paragraph flush

        def flush():
            """Emit the buffered sentences as ONE Word paragraph.

            Each lane keeps the WINDOW of its own sentence inside the joined
            text, so a comment still anchors on the number in the sentence that
            owed it rather than on the first match in the paragraph."""
            if not buf:
                return
            parts, lanes, pos = [], [], 0
            for sent, sl in buf:
                lo = pos
                parts.append(sent)
                pos += len(sent) + 1                      # +1 for the joining space
                hi = pos
                lanes += [(k, v, lo, hi) for k, v in sl]
            d.para_with_comments(" ".join(parts), lanes)
            buf.clear()

        for b in blocks:
            if b[0] == "skipped-lane":
                skipped[b[1]] = skipped.get(b[1], 0) + 1
                continue
            if b[0] == "pbreak":
                flush()
                continue
            if b[0] == "h":
                flush()
                d.heading(b[1], b[2])
                continue
            npara += 1
            rendered, auto = inline.render(b[1])
            sl = auto + [(k, v) for k, v in b[3]]
            for k, _v in sl:
                if k not in lanes:
                    held[k] = held.get(k, 0) + 1
            sl = [(k, v) for k, v in sl if k in lanes]
            if a.join_paragraphs:
                buf.append((rendered, sl))
            else:
                d.para_with_comments(rendered, sl)

            if a.no_displays:
                continue
            for unit, n in list(num.given.items()):
                if unit in placed:
                    continue
                rec = disp.by_unit[unit]
                if rec["kind"] == "table":
                    parsed = parse_table_body(rec["body"])
                    if parsed:
                        rows, align = parsed
                        flush()                            # a float follows the ¶
                        d.table(rows, align=align,
                                caption="Table %d. %s" % (
                                    n, inline.caption(rec["caption"]) or unit))
                    else:
                        report.append(("no-table-body", f"{unit} has no parsable table-body.tex"))
                    placed.add(unit)
                else:
                    img = rec["image"] or (
                        # cache under the PAPER's 3-dist, never the output dir:
                        # a build writing elsewhere (a /tmp test) made its own
                        # cache and re-rasterized every time.
                        rasterize(rec["pdf"],
                                  os.path.join(root, "3-dist", ".media"),
                                  report) if rec.get("pdf") else None)
                    if img:
                        flush()
                        d.image(img, caption="Figure %d. %s" % (
                            n, inline.caption(rec["caption"]) or unit))
                    else:
                        report.append(("no-image",
                                       f"{unit} has neither figure.png nor a "
                                       f"rasterizable figure.pdf"))
                    placed.add(unit)
        flush()

    if inline.cited:
        d.heading(1, "References")
        # one list for the WHOLE document, alphabetical, in MISQ's Reference
        # style: single-spaced with a left hanging indent.
        for k in sorted(inline.cited, key=lambda k: bbl.intext.get(k, k).lower()):
            d.para(bbl.body.get(k, f"[{k}: not in .board-refs.bbl]"),
                   style="Reference")

    d.save(out)

    print(f"✅ {out}")
    print(f"   {len(pages)} page(s) · {npara} paragraphs · "
          f"{d.cid} anchored comments · {len(num.given)} displays placed · "
          f"{len(inline.cited)} references")
    print("   comment lanes: " + ", ".join(lanes)
          + (" · held back by --lanes: "
             + " · ".join(f"{k} {v}" for k, v in sorted(held.items())) if held else ""))
    if skipped:
        print("   working lanes NOT exported (they stay on the board): "
              + " · ".join(f"{k} {v}" for k, v in sorted(skipped.items())))
    if report:
        print(f"⚠️  {len(report)} thing(s) the export could not resolve:")
        seen = set()
        for kind, msg in report:
            if (kind, msg) in seen:
                continue
            seen.add((kind, msg))
            print(f"    {kind:18s} {msg}")


if __name__ == "__main__":
    main()
