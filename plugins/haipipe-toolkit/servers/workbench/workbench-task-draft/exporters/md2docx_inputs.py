"""What the writer reads beside the page: the bibliography, the displays, a compact lane, and TeX made plain."""

import os, re

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
        # convention: a board page's v4 Result payloads live under
        # `<page>/results/<run>/payload/<unit>/` (with the retired
        # `<page>/display/` shape still accepted for compatibility). Without
        # this hook every projection of such a page ships its evidence
        # citations as plain text.
        if extra_root and os.path.isdir(extra_root):
            self._scan(extra_root)

    def _scan(self, base):
        # The paper convention has one level (`displays/<unit>`); v4 Page
        # Results add two levels (`results/<run>/payload/<unit>`). Scanning
        # only immediate children made valid Result payloads invisible to
        # Word RD while the Evidence Space could still render them.
        files = sorted(
            os.path.join(root, name)
            for root, _dirs, names in os.walk(base)
            for name in names if name == "float.tex"
        )
        for f in files:
            unit_dir = os.path.dirname(f)
            unit = os.path.basename(unit_dir)
            tex = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"\\begin\{(table|figure|algorithm)", tex)
            lab = re.search(r"\\label\{([^}]+)\}", tex)
            assets = os.path.join(unit_dir, "assets")
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
            note_match = re.search(
                r"\\begin\{flushleft\}(.*?)\\end\{flushleft\}",
                tex, flags=re.S)
            note = note_match.group(1).strip() if note_match else ""
            rec = {
                "unit": unit,
                # the RAW tex. detex is deferred to emit time so the Resolver can
                # turn a \ref inside the caption into its number first.
                "caption": cap,
                "note": note,
                # Word places algorithm blocks as a raster figure. Its source
                # environment is retained in LaTeX, while the reader-facing
                # Word reference shares the figure sequence.
                "kind": ("table" if m and m.group(1) == "table" else
                         "figure" if m else "unknown"),
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

    A non-greedy `\\enquote\\{(.*?)\\}` stops at the first `}` it meets, and a
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
    # A `\\` inside a command argument (most commonly `\\shortstack`) is a
    # visual line break, not a Word table row. Keep the header in one cell.
    s = re.sub(r"\\\\", " ", s)
    # SUPERSCRIPTS. `$^{***}$` lost its delimiters above and then its braces
    # below, so every significance star in every table cell shipped as the
    # literal `9.3438^***` (JL 2026-07-28). Word can superscript a run, but this
    # function returns plain text, and bare `***` is the reading convention in a
    # results table anyway. Digits become real superscript characters.
    s = re.sub(r"\^\{?(\*+)\}?", r"\1", s)
    s = re.sub(r"\^\{?([0-9])\}?", lambda m: SUPER[int(m.group(1))], s)
    s = s.replace("~", " ").replace("--", "\u2013").replace("\\&", "&")
    # BibTeX's line-break hint takes a NUMBER: plainnat writes
    # `376\penalty0 (7):\penalty0 663--673`. The catch-all below removed only
    # `\penalty` and every reference shipped as "3760 (7):0 663–673" (JL 260928).
    s = re.sub(r"\\penalty\s*(?:-?\d+|\\@M)\s*", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()
