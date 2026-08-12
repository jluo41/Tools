"""The `paper` dialect: resolve a manuscript's inline markers at BUILD time.

A board declares this in board.md:

    dialect: paper
    paper-root: ..

and then `\\citep{key}` in a sentence stops being grey prose and becomes a chip
that knows whether the key exists.

WHY BUILD TIME. The board's invariant is that stripping every <script> leaves
the substance intact. Evidence resolved in JavaScript would vanish under that
test. So the index is built once, here, and each chip ships with a `title=`,
which is a native browser tooltip: hover already works with no script at all.
JavaScript may later upgrade that tooltip into a rich card, and it may not be
the only copy of anything.

Citations resolve against the `.bib`; owed markers of every kind resolve
against `1-probes/`, because `[Q-Sec6Results-4]` is not citation grammar or value
grammar, it is the paper's ONE join key from a sentence to the question that
owes it. Displays resolve against the display WORKSPACE (`0-lifecycle/3-display/\nworkspace/`, legacy `displays/`) and are the remaining slice.

THIS MODULE IS DELETABLE. The board must build with it gone and every board
that does not say `dialect: paper` must render byte-identical, which is the
mechanical form of "the board never assumes a paper". build.py asserts it.
"""

import difflib
import os
import re
from pathlib import Path
from urllib.parse import quote_plus

# @article{key,  ...fields...   up to the next entry at column 0
ENTRY = re.compile(r"^@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=^@|\Z)", re.S | re.M)
# title = {...}  /  title = "..."  /  year = 2018
FIELD = re.compile(r"(\w+)\s*=\s*(?:\{(.*?)\}|\"(.*?)\"|(\d+))\s*,?\s*$",
                   re.S | re.M)
BRACES = re.compile(r"[{}]")


def _fields(blob):
    out = {}
    for m in FIELD.finditer(blob):
        val = m.group(2) or m.group(3) or m.group(4) or ""
        out[m.group(1).lower()] = BRACES.sub("", " ".join(val.split()))
    return out


def _surname(who):
    """First author's surname, from either `Last, First` or `First Last`."""
    first = (who or "").split(" and ")[0].strip()
    if not first:
        return ""
    return first.split(",")[0].strip() if "," in first else first.split()[-1]


def _one_line(f):
    """A bibtex entry as one readable line, for a tooltip."""
    who = f.get("author") or f.get("editor") or ""
    if " and " in who:
        who = _surname(who) + " et al."
    elif who:
        who = _surname(who)
    where = (f.get("journal") or f.get("booktitle") or f.get("publisher")
             or f.get("school") or f.get("institution") or "")
    bits = [b for b in (who, f.get("year", ""), f.get("title", ""), where) if b]
    return " · ".join(bits)


# ---------------------------------------------------------------- probes --
# A probe entry names the sentences it serves in its `### q-consumer` block.
# Two decorations are in live use across the folders (`* **Q-Sec7Discussion-2** — …`
# and `- Q-Sec7Discussion-1 (§7.2): …`), so read the ID and ignore the bullet.
# The stage token accepts DIGITS: a stage that `runs: per-unit` names its unit
# in it (`Q-Sec0Abstract-1`), which is the only way nine section units stop
# colliding on one id. Letters-only silently un-chipped every such bracket.
# The executor's drawer of original answers. `QA-BANK` is the name ruled on
# 260806 so the twin law is visible in the filesystem rather than only in the
# contract; `QA` is the pre-rename name and stays readable while the example
# repositories migrate one at a time. Both are accepted; new work writes the
# first.
BANK_DIRS = ("QA-BANK", "QA")

QID = re.compile(r"\bQ-[A-Za-z0-9]+-\d+\b")
CITE_TEX = re.compile(r"\\cite[tp]?\*?\{([^}]*)\}")
REF_TEX = re.compile(r"\\(?:auto|C|c)?ref\{((?:tab|fig):[^}]*)\}")
# what a browser can put in an <img>. A .pdf asset cannot be previewed,
# and the panel says so rather than showing a broken frame.
IMG = (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif")
# The per-asset Display page names its unit in `### What it shows`.  Both the
# current pilot's `Registry id:` and the standard template's `unit:` form are
# accepted. A paired page may deliberately use an alphabetic registry identity
# such as ``display01a`` rather than retaining a misleading legacy sequence.
S_DISPLAY_UNIT = re.compile(
    r"(?im)^\s*(?:registry\s+id|unit)\s*:\s*"
    r"((?:S-Display-\d+[a-z]?(?:[a-z]\d+)?|display\d{2}[a-z]?|"
    r"Q[A-Za-z]*\d+[a-z]?-Display\d+)"
    r"(?:-[a-z0-9-]+)?)\b"
)
# any number as it is written in a probe answer: 1.21494 · 765,701 · 0.001
NUMTOK = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+")

# ---------------------------------------------------- register bindings --
# An evidence page's `### E<n> ·` division (ref/topic-entry-contract.md)
# binds a consumer row's stake to evidence with backticked TOKENS, not prose:
# a bibliography key on the outward route (the citation binding), bank
# provenance paths on the inward one (the value binding). Only these two
# shapes resolve to chips; everything else in backticks stays ordinary code,
# which is how the page's free prose keeps the no-chips ruling (JL 260806).
#   BIBKEY is the surname-year-word shape this family's .bib uses
#   (luo2025mapping, mafi2013association). Requiring the trailing word is
#   what keeps run ids (`v0618`) and spec names (`SPEC5`) out.
BIBKEY = re.compile(r"^[A-Za-z][A-Za-z'-]*\d{4}[a-z][a-z0-9-]*$")
BANK_PATH = re.compile(r"^(?:tasks|discoveries)/\S+$")


# The contract's own slot names, mapped to the keys this parser reads. The two
# disagreed and neither side complained: `ref/topic-entry-contract.md` specifies
# `#### consumer trace` while this parser split on `### ` and looked up
# `q-consumer`, so a record written exactly to the contract parsed to an empty
# `asks`, every `[Q-…]` on its page rendered `unowned`, and nothing anywhere
# said why. Measured 260807 on QBt5: writing the record to the contract gave
# asks=[]; changing the heading level alone still gave asks=[]; only changing
# BOTH gave asks=['Q-Value-1']. Both spellings are accepted, because 28 records
# on the live paper predate the contract and must keep parsing.
SLOT_ALIAS = {"consumer trace": "q-consumer",
              "bank binding": "bank binding",
              "q-executor": "q-executor",
              "a-executor": "a-executor"}


def _sections(text):
    """A probe file split on its `###` or `####` headings, keyed lowercase.

    BOTH LEVELS, because the contract writes the four slots at `####` and this
    split only ever accepted `###`. A record obeying the contract produced no
    sections at all, which is invisible: every downstream field falls back to
    its default and the page renders as if the record simply said nothing.
    """
    out, cur, buf = {}, "", []
    for ln in text.split("\n"):
        h = ln.startswith("#### ") and 5 or (ln.startswith("### ") and 4 or 0)
        if h:
            out[cur] = "\n".join(buf).strip()
            name = ln[h:].strip().lower()
            cur, buf = SLOT_ALIAS.get(name, name), []
        else:
            buf.append(ln)
    out[cur] = "\n".join(buf).strip()
    return out


def _field(block, name):
    """`**state**: answered` and `- state: deferred` are both in use."""
    m = re.search(rf"^[-*\s]*(?:\*\*)?{name}(?:\*\*)?\s*:\s*(.+)$",
                  block, re.M | re.I)
    return m.group(1).strip() if m else ""


# How far the answer is from the prose. Ordered worst-last on purpose: when two
# probe entries serve the same sentence, the one that is FURTHEST along wins,
# because the sentence can be written as soon as any one of them lands.
RANK = {"answered": 0, "read": 1, "commissioned": 2, "planned": 3, "deferred": 4}


class Probe:
    """One `1-probes/PPnn_*/QXn_*.md` entry, as far as a chip needs it."""

    def __init__(self, path, root):
        text = path.read_text(encoding="utf-8", errors="replace")
        secs = _sections(text)
        bind = secs.get("bank binding", "")
        self.path = path
        # relpath, not relative_to: a specimen's records sit BESIDE its paper
        # root rather than under it, where relative_to raises. Third site with
        # this exact shape (see also `rel()` in src/display_unit.py and
        # `disp_rel` above), which is itself worth noticing.
        self.rel = os.path.relpath(path, root).replace('\\', '/')
        self.id = f"{path.parent.name.split('_')[0]}/{path.stem.split('_')[0]}"
        self.title = next((l.lstrip("# ").strip() for l in text.split("\n")
                           if l.startswith("#")), path.stem)
        self.state = (_field(bind, "state").split("·")[0].split("(")[0]
                      .strip().lower() or "planned")
        self.route = _field(bind, "route")
        self.target = _field(bind, "target")
        self.answer = secs.get("a-executor", "")
        # FOLLOW THE TARGET. `self.text` is what a prose number is checked
        # against, and it was this file only. Under the twin naming law the
        # answer lives in the BANK and the probe keeps a digest, so the moment
        # a record is written correctly every number it serves becomes `unver`,
        # which reads as "matches nothing in the run" when the run is simply
        # somewhere this never looked. Measured 260807 on QBt5: 4 of 6 number
        # chips flipped from ok to unver the moment the bank was introduced.
        self.text = text
        bank = _field(bind, "target")
        if bank:
            b = (path.parent / bank).resolve()
            if b.is_file() and b != path.resolve():
                self.text = text + "\n" + b.read_text(encoding="utf-8",
                                                      errors="replace")
        self.asks = sorted(set(QID.findall(secs.get("q-consumer", ""))))

    @property
    def rank(self):
        return RANK.get(self.state, 3)

    def chip(self):
        """-> (state, tooltip) for a sentence that points at this probe.

        `answered` is CHECKED, not believed: a probe may say answered while its
        `### a-executor` block is empty, which is the one contradiction that
        looks finished from the prose side.
        """
        where = f"{self.id} · {self.title}"
        head = " ".join(self.answer.split())[:220]
        if self.state == "answered":
            if not self.answer.strip():
                return ("broken",
                        f"{where}\nstate says answered but its a-executor block "
                        f"is EMPTY. Nothing was harvested; this reads as done "
                        f"and is not.")
            return ("ok", f"{where}\nANSWERED · {head}")
        if self.state == "read":
            return ("owed",
                    f"{where}\nREAD — the bank answers this, but a-executor is "
                    f"not harvested yet.\ntarget: {self.target}")
        if self.state == "deferred":
            return ("parked",
                    f"{where}\nDEFERRED on purpose (cost ceiling), not "
                    f"forgotten.\n{head}")
        return ("owed",
                f"{where}\n{self.state.upper()} · route {self.route or '?'}\n"
                f"target: {self.target}")


# ------------------------------------------------------- the bibliography --
# `refs.py` runs the paper's OWN .bst through bibtex and leaves the result here.
# The dialect only reads it: see QBc5 and refs.py's header for why the write is
# a separate, explicit command.
BBL_ITEM = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}(.*?)"
                      r"(?=\\bibitem|\\end\{thebibliography\})", re.S)
# LaTeX the .bbl emits, in the order it has to be undone
TEX_FIX = [
    (re.compile(r"\\enquote\{(.*?)\}", re.S), "\u201c\\1\u201d"),
    (re.compile(r"\{\\it\s*(.*?)\\/\}", re.S), "\\1"),
    (re.compile(r"\{\\(?:it|bf|em|tt|sc)\s*(.*?)\}", re.S), "\\1"),
    (re.compile(r"\\(?:textit|textbf|emph|texttt|url)\{(.*?)\}", re.S), "\\1"),
    (re.compile(r"\\natexlab\{(.*?)\}"), "\\1"),
    (re.compile(r"\\newblock|\\urlprefix|\\/"), ""),
    (re.compile(r"\\&"), "&"),
    (re.compile(r"\\%"), "%"),
    (re.compile(r"~"), " "),
    (re.compile(r"--"), "\u2013"),
    (re.compile(r"[{}]"), ""),
]


def _detex(s):
    for rx, rep in TEX_FIX:
        s = rx.sub(rep, s)
    return " ".join(s.split())


def _load_bbl(root):
    """key -> the reference string the manuscript will actually print."""
    p = root / ".board-refs.bbl"
    if not p.is_file():
        p = next((q for q in sorted(root.glob("*.bbl"))), None)
    if p is None or not p.is_file():
        return {}
    text = p.read_text(encoding="utf-8", errors="replace")
    return {m.group(1).strip(): _detex(m.group(2))
            for m in BBL_ITEM.finditer(text)}


class Entry:
    """One bibtex entry, with enough to POINT AT it: which file, which line,
    and the raw text as written. The chip's panel shows the entry and links to
    the line, so "does this key exist" and "what is it" are one click, not a
    grep. Nothing here writes: the .bib is human-only."""

    __slots__ = ("key", "fields", "path", "line", "raw")

    def __init__(self, key, fields, path, line, raw):
        self.key, self.fields, self.path = key, fields, path
        self.line, self.raw = line, raw

    def links(self):
        """(label, href) for every way this entry names its own source."""
        f, out = self.fields, []
        doi = f.get("doi", "").strip()
        if doi:
            d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi).strip()
            if d:
                out.append((f"doi {d}", f"https://doi.org/{d}"))
        ep = f.get("eprint", "").strip()
        if ep and "arxiv" in (f.get("archiveprefix", "") + f.get("journal", "")
                              + f.get("primaryclass", "")).lower():
            out.append((f"arXiv:{ep}", f"https://arxiv.org/abs/{ep}"))
        url = f.get("url", "").strip()
        if url.startswith("http") and not any(url == x[1] for x in out):
            short = re.sub(r"^https?://(www\.)?", "", url)
            out.append((short[:58] + ("…" if len(short) > 58 else ""), url))
        # Google Scholar, LAST and with its own glyph, because it is a SEARCH
        # and everything above it is an identifier. A doi resolves to THE work;
        # this resolves to a result page that can be wrong. It earns its place
        # anyway: most pre-doi entries have no other link at all, and on this
        # paper's own .bib only a minority carry one (JL 260726).
        # Title plus first-author surname, and deliberately NO year: a preprint
        # and its published version disagree by one, and the year is the field
        # most likely to exclude the very result you wanted.
        title = f.get("title", "").strip().rstrip(".").strip()
        if title:
            who = _surname(f.get("author") or f.get("editor") or "")
            q = f'"{title}"' + (f" {who}" if who else "")
            out.append(("Scholar", "https://scholar.google.com/scholar?q="
                        + quote_plus(q), "🔎"))
        return out


def _short(uid):
    r"""The stable prefix a page may write instead of the full unit name.

    `S-Display-4a-main-regression` -> `S-Display-4a`, `display04a-main-regression`
    -> `display04a`. Splitting on the first hyphen was right when every id began
    with `display`; under the workspace layout the first two hyphens belong to
    the `S-Display-` prefix itself, and splitting there would key every unit on
    the string `S`, collapsing the whole set onto whichever sorted first.

    THE VARIANT TAIL IS PART OF THE KEY. A letter plus a tail is the same claim
    under a different specification (`4al2` and `4al5` are the main regression on
    the binary and continuous exposures). Stopping at the letter would return
    `S-Display-4a` for both, so `by_short` would keep whichever sorted first and
    the other would be unreachable by its short form (JL 260728).
    """
    m = re.match(
        r"(S-Display-\d+[a-z]?(?:[a-z]\d+)?|display\d{2}[a-z]?|"
        r"Q[A-Za-z]*\d+[a-z]?-Display\d+)",
        uid,
    )
    return m.group(1) if m else uid.split("-", 1)[0]


class Display:
    """One display unit folder, as far as a chip needs it.

    Named `S-Display-<id>-<slug>/` under the workspace layout, after the page
    that owns it, or `displayNN[a]-<slug>/` under the legacy one.

    The unit's own float.tex is the authority on two things a sentence needs:
    what KIND it is (`\\begin{table}` vs `\\begin{figure}`, which is why QC3 and
    QC4 are two pages) and what `\\label{}` the manuscript may point at.
    """

    __slots__ = ("id", "path", "kind", "label", "assets", "candidates",
                 "versions", "pptx", "data", "stale", "takeaway", "placement",
                 "preview", "preview_img", "preview_stale", "float_target")

    def __init__(self, d, root):
        self.id, self.path = d.name, d
        float_tex = d / "float.tex"
        ft = float_tex.read_text(encoding="utf-8", errors="replace") \
            if float_tex.is_file() else ""
        m = re.search(r"\\begin\{(table|figure)\*?\}", ft)
        self.kind = m.group(1) if m else "figure"
        m = re.search(r"\\label\{([^}]*)\}", ft)
        self.label = m.group(1) if m else ""
        # The printable wrapper is authoritative about the live artifact.  A
        # Board must show that file separately from preview.pdf, otherwise a
        # stale or legacy wrapper hides what the manuscript is actually using.
        self.float_target = None
        for pat in (r"\\includegraphics(?:\[[^]]*\])?\{([^}]*)\}",
                    r"\\input\{([^}]*)\}"):
            m = re.search(pat, ft)
            if not m:
                continue
            raw = m.group(1).strip()
            candidate = (root / raw).resolve()
            if candidate.is_file():
                self.float_target = candidate
                break
        self.assets = _names(d / "assets")
        self.candidates = _names(d / "candidates")
        self.versions = _names(d / "versions")
        # A PPTX is an editable authoring source, never the paper's printable
        # artifact. Prefer the new `recipe/` home, but surface legacy copies so
        # a Board can still point a human to the file they may repair. The
        # compiled float below remains the review truth.
        self.pptx = []
        for folder, role in (("recipe", "editable"), ("source", "legacy"),
                             ("candidates", "candidate"), ("versions", "version")):
            for p in sorted((d / folder).glob("*.pptx")):
                self.pptx.append((role, p))
        # New units read the approved intake snapshot.  Legacy source/ units
        # remain inspectable until an explicit provenance-safe migration.
        self.data = next((p for p in (d / "intake" / "inputs").glob("source_data.*")), None)
        if self.data is None:
            self.data = next((p for p in (d / "source").glob("source_data.*")), None)
        # STALE: the numbers were re-run after the asset was built. The unit
        # looks finished and the manuscript is showing the older picture.
        newest = max((p.stat().st_mtime for p in (d / "assets").glob("*")),
                     default=0)
        self.stale = bool(self.data and newest
                          and self.data.stat().st_mtime > newest)
        # preview.pdf is float.tex COMPILED STANDALONE: the graphic or the rows,
        # plus the caption, the notes and the numbering, set by the paper's own
        # class. It is to a Display what the .bbl is to a citation, so the panel
        # shows it on the same terms (JL 260726). It is also the only way a TABLE
        # unit can be seen at all: those carry no image, and the panel had been
        # showing LaTeX source where a reader wanted rows.
        pv = d / "preview.pdf"
        self.preview = pv if pv.is_file() else None
        # A PDF only renders where the browser has a PDF viewer. VS Code's
        # webview does not, so `<object type=application/pdf>` fell back to a
        # bare link and every display panel on every page was an empty box
        # (JL 260727, "WHERE IS THE DISPLAY"). A raster of the same compiled
        # float renders in an <img> everywhere, so it is preferred when present
        # and the PDF stays reachable beside it.
        #   regenerate: pdftocairo -png -r 130 -singlefile preview.pdf preview
        pvi = d / "preview.png"
        self.preview_img = pvi if pvi.is_file() else None
        # A preview built before the asset it previews is worse than none, so it
        # is labelled rather than hidden: the reader decides what to trust.
        self.preview_stale = bool(self.preview and newest
                                  and pv.stat().st_mtime < newest)
        # A View-owned Display keeps its human contract in output.md and also
        # carries the generic renderer's README.md.  Prefer output.md for the
        # owner-indexed View identity; otherwise the renderer README would hide
        # the reader takeaway and View-body bindings from the rich Card.  Paper
        # and legacy units continue to prefer README.md.
        view_owned = bool(re.match(r"Q[A-Za-z]*\d+[a-z]?-Display\d+", self.id))
        rd = d / ("output.md" if view_owned else "README.md")
        if not rd.is_file():
            rd = d / ("README.md" if view_owned else "output.md")
        txt = rd.read_text(encoding="utf-8", errors="replace") if rd.is_file() else ""
        self.takeaway = _para(txt, "Reader Takeaway")
        self.placement = _para(txt, "Placement")

    def chip(self):
        """-> (state, tooltip). Reported worst-first: a stale unit that also has
        candidates is reported STALE, because that is the one that misleads."""
        head = f"{self.id} · {self.kind}" + (f" · {self.label}" if self.label else "")
        tail = ("\n" + self.takeaway) if self.takeaway else ""
        if not self.assets:
            return ("owed", f"{head}\nREQUESTED — the unit exists and nothing is "
                            f"built in assets/ yet.{tail}")
        if self.stale:
            also = (f"\nIt ALSO has {len(self.candidates)} candidate(s) waiting: "
                    f"{', '.join(self.candidates)}") if self.candidates else ""
            return ("broken", f"{head}\nSTALE — {self.data.name} was re-run AFTER "
                              f"{'/'.join(self.assets[:2])} was built. The "
                              f"manuscript is showing the older numbers.{also}{tail}")
        if self.candidates:
            return ("ready", f"{head}\nCANDIDATE waiting: "
                             f"{', '.join(self.candidates)}\nassets/ still holds "
                             f"{', '.join(self.assets)}, so the compiled paper "
                             f"shows the OLD one.{tail}")
        return ("ok", f"{head}\n{', '.join(self.assets)}"
                      + (f" · {len(self.versions)} superseded"
                         if self.versions else "") + tail)


def _names(d):
    return sorted(p.name for p in d.glob("*")
                  if p.is_file() and p.name != ".gitkeep") if d.is_dir() else []


def _para(txt, heading):
    m = re.search(rf"^#+\s*{heading}\s*$(.*?)(?=^#|\Z)", txt, re.S | re.M)
    return " ".join(m.group(1).split())[:200] if m else ""


class Paper:
    """One paper's resolvable index. Built once per board build."""

    def __init__(self, root):
        self.root = Path(root)
        self.bib = {}
        self.bib_files = []
        # A View owns its editable bibliography under input/sources/.  Paper
        # roots historically kept .bib files at the root.  Read both shapes,
        # while excluding generated review builds so a copied bibliography is
        # never indexed twice.
        for p in sorted(self.root.rglob("*.bib")):
            if any(part in ("build", "_archive") or part.startswith(".")
                   for part in p.relative_to(self.root).parts):
                continue
            self.bib_files.append(p.relative_to(self.root).as_posix())
            text = p.read_text(encoding="utf-8", errors="replace")
            for m in ENTRY.finditer(text):
                key = m.group(1).strip()
                if key in self.bib:
                    continue
                self.bib[key] = Entry(key, _fields(m.group(2)), p,
                                      text.count("\n", 0, m.start()) + 1,
                                      m.group(0).rstrip().rstrip(","))
        # Displays, and the LaTeX labels the whole paper declares. The label
        # index spans every .tex, not just displays/, because a \ref{} that
        # resolves to a section-local label is fine; one that resolves to
        # NOTHING compiles to `??` and is the defect worth naming.
        # WHERE THE UNITS LIVE. Two layouts, and the board always reads the
        # SOURCE one, because candidates/, versions/ and preview.png exist only
        # there and a card without them cannot be judged.
        #   workspace (current):  0-lifecycle/3-display/workspace/S-Display-<id>-<slug>/
        #                         `displays/` is a BUILD TARGET carrying float
        #                         + assets only, generated by build-displays.py,
        #                         the same relationship `sections/` has to the
        #                         S-Main pages.
        #   legacy:               displays/display<NN><a>-<slug>/ was the source
        # A unit folder now shares its NAME with the S-Display page that owns
        # it, which is what retires the derived join in `_sdisplay_read` below.
        # FIND the workspace by SHAPE, never by a fixed folder name (260803).
        # This was pinned to `0-lifecycle/3-display/`, and the day the board's
        # folders were renamed after their GROUP, `S05-display/`, the pin missed
        # and every display page silently fell back to the legacy `displays/`
        # tree, which rendered nine preview images at an href that resolves
        # nowhere. A group folder may be renamed again; `*/workspace` may not.
        # BOTH names for the authoring folder, and the specimen layout too.
        # This tried `workspace` ONLY. The folder was renamed to `display` on
        # 260806 and nothing here noticed: the live MISQ paper fell through to
        # the legacy `displays/display*` branch and indexed ZERO units, so every
        # evidence card and every \ref chip on that board silently stopped
        # resolving while each page still looked finished. Measured 260807.
        lc = self.root / "0-lifecycle"
        ws = None
        for d in (sorted(lc.glob("*display*")) if lc.is_dir() else []):
            ws = next((d / n for n in ("display", "workspace")
                       if (d / n).is_dir()), None)
            if ws:
                break
        # A SPECIMEN root carries its own paper root under `_fixture/`, so the
        # authoring folder is that root's SIBLING rather than its descendant.
        if ws is None and (self.root.parent / "display").is_dir():
            ws = self.root.parent / "display"
        if ws is not None:
            # `*` and not `S-Display-*`: the prefix is one paper's page-naming
            # convention, and `float.tex` is what actually makes a folder a unit.
            self.disp_dir, self.disp_glob = ws, "*"
        else:
            # A legacy paper root may now contain owner-indexed View Displays
            # such as `QBt1-Display1-main-table`. The float wrapper, not a
            # filename prefix, is the authority for whether a child is a unit.
            view_output = self.root / "output"
            if view_output.is_dir():
                self.disp_dir, self.disp_glob = view_output, "*"
            else:
                self.disp_dir, self.disp_glob = self.root / "displays", "*"
        # `os.path.relpath`, not `relative_to`: on a real paper the authoring
        # folder is BELOW the paper root, and on a specimen root it is beside
        # it, where `relative_to` raises instead of walking up. Same fix, and
        # the same reason, as `src/display_unit.py`'s `rel()`.
        self.disp_rel = os.path.relpath(self.disp_dir, self.root).replace("\\", "/")
        # Path PARTS that hold a float and therefore declare rather than cite.
        # Under the workspace layout that is BOTH trees: the generated
        # `displays/` carries a copy of every float, so indexing it would
        # declare every \label{} twice and report a collision against itself.
        self.disp_parts = {self.disp_dir.name, "displays"}
        self._sd_cache = {}     # unit id -> (S-Display id, its state: line)
        self.displays = {}
        self.by_short = {}      # "display02" -> the unit; the S-Display pages
        self.by_label = {}      # write the short form, a Section the long one
        for d in sorted(self.disp_dir.glob(self.disp_glob)):
            # `float.tex` IS the unit test, which is what makes the `*` glob
            # above safe: `_archive/`, a README and any other stray sibling
            # carry none and are skipped without needing a name rule.
            if d.is_dir() and not d.name.startswith("_") and (d / "float.tex").is_file():
                u = Display(d, self.root)
                self.displays[u.id] = u
                self.by_short.setdefault(_short(u.id), u)
                if u.label:
                    self.by_label.setdefault(u.label, u)
        self.labels = {}
        for p in sorted(self.root.rglob("*.tex")):
            if "_archive" in p.parts or ".claude" in p.parts:
                continue
            t = p.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"\\label\{([^}]*)\}", t):
                self.labels.setdefault(
                    m.group(1), (p, t.count("\n", 0, m.start()) + 1))
        self.printed = self._input_closure()
        self.refs = _load_bbl(self.root)
        # A probe's `target:` is written relative to the PROJECT, not the paper:
        # `tasks/Z01_…/QA/4-….md`. Find the folder those resolve against by
        # walking up for the banks themselves, rather than assuming a depth.
        self.bank_root = None
        here = self.root
        for _ in range(4):
            if (here / "tasks").is_dir() or (here / "discoveries").is_dir():
                self.bank_root = here
                break
            if here.parent == here:
                break
            here = here.parent
        self.probes = []
        self.by_q = {}
        # FIND RECORDS BY SHAPE, not by one fixed path and one filename prefix.
        # This read `(root/"1-probes").rglob("QX*.md")` and nothing else. The
        # folder was renamed to `probes/<topic>/` on the live paper and to
        # `QA-probe/<page>/` by JL's 260806 ruling, and the records are named
        # `<n>-<slug>.md` by that same contract, so BOTH halves stopped matching
        # and `rglob` returned []. Measured 260807: 0 probes on the MISQ paper,
        # which has 28 of them, and 0 on the specimen, which has 2. Zero probes
        # renders every `[Q-…]` on every page as `unowned`, and says nothing.
        roots = [self.root]
        # A specimen root carries its own paper root under `_fixture/`, so its
        # records sit beside that root rather than under it.
        if self.root.name == "_fixture":
            roots.append(self.root.parent)
        found = []
        for base in roots:
            for d in sorted(base.rglob("*")):
                if not d.is_dir() or d.name not in (
                    "probes", "QA-probe", "QA-probes", "1-probes"
                ):
                    continue
                if any(x.startswith(("_", ".")) for x in d.parts):
                    continue
                found += [f for f in sorted(d.rglob("*.md")) if f.is_file()]
        for p in found:
            pr = Probe(p, self.root)
            self.probes.append(pr)
            for q in pr.asks:
                self.by_q.setdefault(q, []).append(pr)
        for q, ls in self.by_q.items():
            ls.sort(key=lambda pr: pr.rank)

    def _near(self, key):
        """Keys a broken one might have MEANT, best first.

        Plain fuzzy matching is not enough here: `stock2005testing` against
        `stock2002survey` scores ~0.6 and falls off the edge of the default
        cutoff, which is exactly the case that matters. Bibtex keys are
        author-year-word, so the author run is the strong signal and is matched
        directly; fuzz only fills in behind it.
        """
        stem = re.match(r"[A-Za-z]+", key)
        out = []
        if stem:
            s = stem.group(0).lower()
            out = sorted(k for k in self.bib
                         if k.lower().startswith(s) and k != key)
        for k in difflib.get_close_matches(key, self.bib, n=4, cutoff=0.55):
            if k not in out and k != key:
                out.append(k)
        return out[:3]

    # -- citations ----------------------------------------------------------
    def citation(self, key):
        """-> (state, label, tooltip, meta).

        `meta` is DATA, never html: the dialect resolves and the board renders
        (QBc5). Keys: `entry` (path, line, raw bibtex), `links` (label, href to
        the actual source), `suggest` (near-miss keys, for a broken one).
        """
        e = self.bib.get(key)
        if e is None:
            near = self._near(key)
            tip = f"NOT IN .bib — {key} does not resolve and will compile to [?]"
            if near:
                tip += "\nDid you mean: " + ", ".join(near)
            return ("broken", key, tip,
                    {"suggest": [(k, _one_line(self.bib[k].fields))
                                 for k in near]})
        ref = self.refs.get(key)
        return ("ok", key, (ref or _one_line(e.fields) or key),
                {"entry": e, "links": e.links(), "reference": ref})

    # -- register bindings ---------------------------------------------------
    def register_binding(self, tok):
        """-> (kind, state, label, tip, meta) for one backticked token inside
        an evidence page's `### E<n> ·` division, or None when the token is
        not a binding shape and must keep its ordinary code rendering.

        The citation side reuses citation() whole, so a register key opens the
        same card a prose \\citep chip does: the .bib entry, its line, the
        source links, the rendered reference. A key-shaped token that does NOT
        resolve is exactly the defect the register exists to surface, so it
        renders broken rather than silently grey. The value side resolves the
        row's provenance paths against the bank and NEVER invents: a path that
        is not on disk renders owed, with the miss stated.
        """
        if BANK_PATH.match(tok):
            state, label, tip, meta = self.bank_binding(tok)
            return ("val", state, label, tip, meta)
        if tok in self.bib or BIBKEY.match(tok):
            state, label, tip, meta = self.citation(tok)
            return ("cite", state, label, tip, meta)
        return None

    def bank_binding(self, tok):
        """-> (state, label, tip, meta) for a value binding's provenance path.

        BOUND on the inward route means a run you can walk to
        (haipipe-page-for-value), so the card carries the path as links:
        the file itself and the run folder it belongs to, the same shape
        chain() gives a number chip. The label is the path's tail; the full
        path stays in the tip and on the card's 🎯 line.
        """
        label = "/".join(tok.split("/")[-2:])
        if self.bank_root is None:
            return ("unowned", label,
                    f"{tok}\nNO BANK: no tasks/ or discoveries/ folder was "
                    f"found above the paper root, so this path resolves "
                    f"against nothing.", {"target": tok})
        p = self.bank_root / tok
        if p.is_file():
            files = [(f"answer · {p.name}", p)]
            folder = p.parent.parent if p.parent.name.upper() in BANK_DIRS \
                else p.parent
            if folder.is_dir() and folder != self.bank_root:
                files.append((f"run · {folder.name}/", folder))
            tip = f"{tok}\nresolves in the bank."
            if p.suffix.lower() == ".md":
                head = p.read_text(encoding="utf-8", errors="replace")[:600]
                st = re.search(r"^state:\s*(.+)$", head, re.M)
                if st:
                    tip += f"\nQA state: {st.group(1).strip()}"
            return ("ok", label, tip, {"files": files, "target": tok})
        if p.is_dir():
            return ("ok", label,
                    f"{tok}\nresolves to a run folder in the bank.",
                    {"files": [(f"run · {p.name}/", p)], "target": tok})
        return ("owed", label,
                f"{tok}\nDOES NOT RESOLVE under {self.bank_root.name}/. "
                f"The row stays open: a value binding is only BOUND when its "
                f"run, spec and QA paths exist on disk.", {"target": tok})

    # -- the [Q-X-n] join key -----------------------------------------------
    def question(self, qid):
        """-> (state, tooltip, meta) for a bracket. `unowned` means NO probe
        entry declares this id, so the bracket promises a question nobody is
        holding. `meta` carries the probe file so the panel can link to it."""
        ls = self.by_q.get(qid)
        if not ls:
            return ("unowned",
                    f"{qid} is claimed by NO probe entry. Nothing in 1-probes/ "
                    f"declares it under ### q-consumer, so nothing will resolve "
                    f"this marker.", {})
        state, tip = ls[0].chip()
        if len(ls) > 1:
            tip += f"\n(+{len(ls) - 1} more probe entr" \
                   f"{'y' if len(ls) == 2 else 'ies'} serve {qid})"
        return (state, tip, {"files": self.chain(ls)})

    # -- the manuscript the board does NOT render ---------------------------
    def audit(self):
        """Unresolved markers in the paper's own `.tex`, which no chip can show.

        A chip only exists where the board renders text, and the board renders
        its pages. `sections/*.tex` (`0-sections/` pre-QA6) is the manuscript and is reached
        only when a page embeds it, so a broken key can sit there compiling to
        `[?]` with a clean-looking board. This walks the tex directly and hands
        build.py a list to print. Reporting is all it does: the `.bib` is
        human-only and nothing here writes.
        """
        out = []
        for p in sorted(self.root.rglob("*.tex")):
            if "_archive" in p.parts or self.disp_parts & set(p.parts):
                continue
            for i, ln in enumerate(p.read_text(encoding="utf-8",
                                               errors="replace").split("\n"), 1):
                bare = re.sub(r"(?<!\\)%.*$", "", ln)      # drop LaTeX comments
                for m in CITE_TEX.finditer(bare):
                    for k in (x.strip() for x in m.group(1).split(",")):
                        if not k:
                            continue
                        if k.upper() == "TOADD":
                            if not re.match(r"\s*\[Q-[A-Za-z0-9]+-\d+\]", bare[m.end():]):
                                out.append((p.relative_to(self.root).as_posix(),
                                            i, "unowned", r"\cite{TOADD} with no [Q-…]"))
                        elif k not in self.bib:
                            out.append((p.relative_to(self.root).as_posix(),
                                        i, "broken", f"\\citep{{{k}}} is not in the .bib"))
                for m in REF_TEX.finditer(bare):
                    if m.group(1) not in self.labels:
                        # `unowned`, not `broken`, and deliberately: the CHIP for
                        # this same marker renders `unowned` (QC3's legend: "the
                        # id, or the \ref{} label, resolves to nothing"), while
                        # `broken` on a display means STALE. One fact, one word.
                        out.append((p.relative_to(self.root).as_posix(), i,
                                    "unowned",
                                    f"\\ref{{{m.group(1)}}} resolves to no "
                                    f"\\label anywhere; it compiles to ??"))
        # QD6's ⑥-empty diagnostic: a display nothing points at is a leftover.
        cited = set()
        for p in self.root.rglob("*.tex"):
            if "_archive" in p.parts or ".claude" in p.parts:
                continue
            if self.disp_parts & set(p.parts):   # a unit's own float.tex
                continue                         # declares, it does not cite
            cited |= set(REF_TEX.findall(
                p.read_text(encoding="utf-8", errors="replace")))
        for u in self.displays.values():
            if u.label and u.label not in cited:
                out.append((f"{self.disp_rel}/{u.id}/float.tex", 0, "uncited",
                            f"\\label{{{u.label}}} is referenced by no section"))
        return out

    # -- the chain from a number back to the run ----------------------------
    def chain(self, probes):
        """(label, path) for every link between a sentence and its run (QD6).

        A value's provenance is four hops, and until now the chip showed one.
        The probe entry says which question; the bank's QA file says what was
        found; the task or discovery FOLDER is where it was actually computed.
        Each is a real path or it is not offered at all: a link that 404s is
        worse than no link, because it looks like provenance.
        """
        out, seen = [], set()
        for pr in probes:
            if pr.path not in seen:
                seen.add(pr.path)
                out.append((f"probe · {pr.rel}", pr.path))
            t = (pr.target or "").split()[0] if pr.target else ""
            if not t or t in ("NEW", "adjacent") or self.bank_root is None:
                continue
            qa = self.bank_root / t
            if qa.is_file() and qa not in seen:
                seen.add(qa)
                out.append((f"answer · {qa.name}", qa))
            # the run itself: the task or discovery folder the QA file sits in
            folder = qa.parent.parent if qa.parent.name.upper() == "QA" \
                else qa.parent
            if folder.is_dir() and folder != self.bank_root and folder not in seen:
                seen.add(folder)
                out.append((f"run · {folder.name}/", folder))
        return out

    # -- a number in the prose, against the run that produced it ------------
    def check_number(self, qid, raw):
        """Does this prose number appear in the probe that owes the sentence?

        Matching is NUMERIC and precision-aware, never string equality: the
        prose rounds, so `1.21` has to match a recorded `1.21494`. It rounds the
        recorded number to the prose's own decimals and compares.

        A non-match is NOT a defect and is never reported as one. `21% higher
        odds` is derived from an odds ratio of 1.21 and will legitimately never
        appear; so will a threshold the design chose rather than measured. Only
        a MATCH is an assertion. Everything else says it could not be checked.
        """
        ls = self.by_q.get(qid)
        if not ls:
            return ("unowned", f"{raw} points at {qid}, which NO probe entry "
                               f"declares. Nothing can check this number.", {})
        try:
            want = float(raw.replace(",", ""))
        except ValueError:
            return ("unver", f"{raw} could not be read as a number.",
                    {"files": self.chain(ls)})
        dec = len(raw.split(".")[1]) if "." in raw else 0
        # Collect every DISTINCT recorded value that rounds to the prose number,
        # not the first one found. Repeated occurrences of one value are one
        # match; two different values are an AMBIGUITY, and saying "matches"
        # there is a false reassurance of exactly the kind this exists to catch.
        # Live case: `1.21` rounds to both 1.21494 (the binary-exposure odds
        # ratio the sentence means) and 1.20879 (a CI bound of the CONTINUOUS
        # exposure). Reporting either one alone would assert the wrong run.
        hits = {}
        for pr in ls:
            for m in NUMTOK.finditer(pr.text):
                try:
                    got = float(m.group(0).replace(",", ""))
                except ValueError:
                    continue
                if round(got, dec) != round(want, dec):
                    continue
                ctx = " ".join(pr.text[max(0, m.start() - 80):
                                       m.end() + 80].split())
                # WHERE it was found matters. A figure in the `### a-executor`
                # block is the ANSWER. The same digits in the question text or
                # the bank binding are a threshold the question named, or a path
                # like v0618, and calling that a match would overclaim.
                where = "answer" if m.group(0) in pr.answer else "question text"
                hits.setdefault(got, (m.group(0), f"{pr.id} {where}", ctx, pr))
        if len(hits) == 1:
            got, (shown, pid, ctx, pr) = next(iter(hits.items()))
            exact = "" if got == want else f" (recorded as {shown})"
            return ("ok", f"{raw} MATCHES the run{exact}.\n{pid} · …{ctx}…",
                    {"files": self.chain([pr])})
        if len(hits) > 1:
            lines = [f"{raw} is AMBIGUOUS: {len(hits)} DIFFERENT recorded "
                     f"figures round to it, so the run behind this number "
                     f"cannot be identified from the prose alone."]
            for got, (shown, pid, ctx, _pr) in sorted(hits.items()):
                lines.append(f"· {shown} — {pid} · …{ctx}…")
            # every probe involved, so both candidate runs are one click away
            return ("amb", "\n".join(lines),
                    {"files": self.chain([h[3] for h in
                                          (hits[k] for k in sorted(hits))])})
        return ("unver",
                f"{raw} does not appear in {qid}'s answer.\nThat is not by "
                f"itself wrong: a derived figure, a percentage computed from a "
                f"ratio, or a threshold the design chose rather than measured "
                f"will never appear. It means this number was NOT checked.\n"
                f"{ls[0].id} · {ls[0].title}", {"files": self.chain(ls)})

    # -- displays -----------------------------------------------------------
    def _preview(self, u):
        """What the panel should SHOW rather than link to.

        A figure's evidence is the picture, so the picture goes in the panel.
        QC4's law then binds: every image is labelled LIVE or CANDIDATE, because
        a card showing one picture while another is what the manuscript compiles
        is worse than a card showing nothing. A .pdf ASSET still cannot be an
        <img>; the unit's compiled float can, and leads, because it is the float
        as the manuscript will set it.

        A table's evidence is its rows, so the table body is shown as text. That
        is QC3's "preview of the table itself, not a thumbnail of one".
        """
        out = []
        stale = " ⚠️ OLDER THAN THE ASSET" if u.preview_stale else ""
        # The rasterized Current Float leads because it works in the VS Code
        # browser where an embedded PDF may fall back to a link. This is the
        # exact surface a person judges; the PDF remains available immediately
        # below it at full fidelity.
        if u.preview_img is not None:
            out.append(("img",
                        "AS THE FLOAT WILL PRINT · preview.png" + stale,
                        u.preview_img, ""))
        # The ASSET leads, because it IS the figure, cropped to the artwork the
        # float sets. preview.* is a whole letter page with the figure adrift in
        # white, which reduced the actual evidence to a thumbnail. A .pdf asset
        # cannot be an <img>, but it is a real readable display as an <object>,
        # which is exactly what body.py renders for the "pdf" kind.
        for a in u.assets:
            if a.lower().endswith(".pdf"):
                out.append(("pdf", f"LIVE · {a}", u.path / "assets" / a, ""))
            elif a.lower().endswith(IMG):
                out.append(("img", f"LIVE · {a}", u.path / "assets" / a, ""))
        # The compiled float follows: it is the only view that shows the caption
        # typeset under the figure. preview.png is NOT shown, because it is the
        # same page at lower fidelity and it was what buried the asset.
        if u.preview is not None:
            out.append(("pdf",
                        "AS THE FLOAT WILL PRINT, caption included · preview.pdf" + stale,
                        u.preview, ""))
        for c in u.candidates:
            if c.lower().endswith(IMG):
                out.append(("img", f"CANDIDATE · {c}",
                            u.path / "candidates" / c, ""))
        for a in u.assets:
            if a.lower().endswith(".tex"):
                p = u.path / "assets" / a
                body = p.read_text(encoding="utf-8", errors="replace")
                lines = body.split("\n")
                txt = "\n".join(lines[:40])
                if len(lines) > 40:
                    txt += f"\n… {len(lines) - 40} more lines"
                out.append(("text", f"LIVE · {a}", p, txt))
        return out

    def _dmeta(self, u):
        links = []
        for name, p in (("preview.png", u.preview_img),
                        ("preview.pdf", u.preview),
                        ("float.tex", u.path / "float.tex"),
                        ("output.md", u.path / "output.md"),
                        ("README", u.path / "README.md"),
                        (u.data.name if u.data else "", u.data)):
            if name and p and p.is_file():
                links.append((name, p))
        for a in u.assets:
            links.append((a, u.path / "assets" / a))
        for c in u.candidates:
            links.append((f"candidate {c}", u.path / "candidates" / c))
        for role, p in u.pptx:
            links.append((f"PPTX {role} · {p.name}", p))
        sd, sdstate = self._sdisplay(u)
        return {"files": links, "target": u.placement or "",
                "sdisplay": sd, "sdstate": sdstate,
                "preview": self._preview(u)}

    def _sdisplay(self, u):
        r"""-> (S-Display face id, that page's own `state:` line).

        WHY THIS EXISTS. The panel's takeaway comes from the unit's README, and
        on this paper the README is wrong about the unit's state for EIGHT of
        eight units checked (QC3/QC4, 260727): `display03`'s says `rendered`
        where its S-Display page says `⏸️ FOLDED, never \input standalone`.
        The S page is the authority, so the panel now carries a one-click link
        to it AND quotes its state line, rather than presenting the README's
        version of reality with no way to check it.
        `displayNN[a]-<slug>` -> `S-Display-N[A]`, which is how the `> Display:`
        lanes on this paper spell the target.  The optional letter keeps paired
        Display registry identities aligned with their S page without changing
        LaTeX's printed figure counter.

        Cached: every chip asks twice now, once to gate its state and once to
        build its panel, and the lookup walks the tree.
        """
        if u.id in self._sd_cache:
            return self._sd_cache[u.id]
        self._sd_cache[u.id] = out = self._sdisplay_read(u)
        return out

    def _sdisplay_read(self, u):
        # WORKSPACE LAYOUT: the folder is NAMED for its page, so the join is a
        # lookup and not a guess. This is the whole point of the rename. The
        # derived branch below could return a face id for a page that does not
        # exist, hand back an empty state, and let a 🔴 unit paint green.
        direct = sorted(self.root.rglob(f"{u.id}.md"))
        for f in direct:
            if "_archive" in f.parts:
                continue
            head = f.read_text(encoding="utf-8", errors="replace")[:1200]
            st = re.search(r"^state:\s*(.+)$", head, re.M)
            # The face id must carry the VARIANT TAIL. `4al2` and `4al5` are two
            # pages, and stopping at the letter gave both the anchor `S-Display-4A`,
            # which exists on neither, so both cards silently lost their page link.
            m = re.match(r"S-Display-(\d+)([a-z]?(?:[a-z]\d+)?)", u.id)
            sid = (f"S-Display-{m.group(1)}{m.group(2).upper()}" if m
                   else u.id)
            return (sid, st.group(1).strip() if st else "")

        # VIEW LAYOUT: the Display is not another Board Page.  Its own
        # output.md carries the independent acceptance line, so no same-named
        # root adapter is needed merely to make a rich Display Card honest.
        output = u.path / "output.md"
        if output.is_file():
            head = output.read_text(encoding="utf-8", errors="replace")[:1600]
            st = re.search(r"^state:\s*(.+)$", head, re.M)
            if st:
                return (_short(u.id), st.group(1).strip())

        # LEGACY LAYOUT: derive the page name from the unit id. Kept so a paper
        # that has not migrated still builds; it is the fragile path and the
        # workspace layout exists to avoid it.
        m = re.match(r"display0*(\d+)([a-z]?)", u.id)
        if not m:
            return ("", "")
        number, suffix = m.group(1), m.group(2)
        sid = "S-Display-%s%s" % (number, suffix.upper())
        stem = "S-Display-%s%s-" % (number, suffix)
        for f in sorted(self.root.rglob(stem + "*.md")):
            if "_archive" in f.parts:
                continue
            head = f.read_text(encoding="utf-8", errors="replace")[:1200]
            st = re.search(r"^state:\s*(.+)$", head, re.M)
            return (sid, st.group(1).strip() if st else "")
        return (sid, "")

    def unit(self, did):
        """`display04` and `display04-main-regression` are the same unit."""
        return self.displays.get(did) or self.by_short.get(did)

    def unit_for_sdisplay(self, content):
        """Return the Display unit declared by one per-asset S-Display page.

        Page identifiers and unit folders share the intentional paired suffix
        when one exists (`1a` -> `display01a`). The explicit unit record is
        still the only safe join; parsing a title would confuse identity with
        a printed figure number.
        """
        m = S_DISPLAY_UNIT.search(content or "")
        return self.unit(m.group(1)) if m else None

    def display(self, did):
        """-> (state, tooltip, meta) for `displayNN[a]` or its long form."""
        u = self.unit(did)
        if u is None:
            return ("unowned", f"{did} names NO unit under {self.disp_rel}/. "
                               f"Nothing owns this id, so a sentence pointing "
                               f"here points at nothing.", {})
        state, tip = self._gate(u, *u.chip())
        return (state, tip, self._dmeta(u))

    # `worst state wins` spans BOTH sources of truth about a unit (QC4, JL
    # 260727). `Unit.chip()` reads DISK: are the assets built, are they stale,
    # is a candidate waiting. The S-Display page records something disk cannot
    # know: whether the unit is AGREED. A unit can be perfectly built and still
    # be one the author has folded away, and before this the chip painted that
    # green. Measured on the MISQ board: 22 chips read `ok` while linking to a
    # page saying folded or blocked, `display03` worst at 10 green chips on a
    # unit JL folded into Figure 2 on 2026-07-10.
    #
    # Only 🔴 and ⏸️ downgrade. 🟡 is the normal condition of a live paper and
    # does not make a citation wrong; downgrading it would amber almost every
    # chip on the board and the distinction would stop informing. So the line
    # is: green means agreed AND built, and anything else means do not lean on
    # this unit yet. The disk state is never discarded, only outranked, and the
    # tooltip says both plus the S page's own words, because a downgrade whose
    # reason is invisible is the defect this replaces.
    GATE = {"🔴": ("owed", "NOT AGREED"), "⏸️": ("parked", "PARKED"),
            "⏸": ("parked", "PARKED")}

    def _gate(self, u, state, tip):
        sid, sdstate = self._sdisplay(u)
        if not sdstate:
            return (state, tip)
        for mark, (gated, word) in self.GATE.items():
            if sdstate.startswith(mark):
                return (gated,
                        f"{tip}\n\n{word} — {sid} says `{sdstate}`.\n"
                        f"Disk says {state.upper()}, and the unit's own page "
                        f"outranks it: whether the assets are built is a "
                        f"different question from whether the paper may lean "
                        f"on them. Open {sid} to see what it is waiting on.")
        return (state, tip)

    def _input_closure(self):
        r"""Every .tex the MASTER actually reaches, resolved.

        WHY. `self.labels` spans every .tex on disk on purpose, so a section-local
        label still resolves. The cost is that "a `\label` exists somewhere" got
        reported as "this pointer works", and those are different questions: a
        float that no reachable section `\input`s declares its label in a file
        LaTeX never opens, so the `\ref` prints `??` while the board paints green.
        Measured on the MISQ board 260728: `tab:descriptives` read ok EIGHT times
        on one page and prints `??`, and `tab:main_results` read ok while its only
        declaration sits in a retired `_old/` file behind an orphan section.
        """
        # WHICH MASTER. A paper may ship from a GENERATED tree while an older
        # hand-written one still builds beside it. On the MISQ board that is
        # `3-dist/tex/paper.tex`, which `md2tex.py` fills one-way from the S-Main
        # pages, against a legacy root master over `sections/`. Measuring the
        # legacy one reported `??` for nine displays that were in the shipped PDF
        # all along, so the generated tree wins when it exists (JL 260728).
        dist = self.root / "3-dist" / "tex" / "paper.tex"
        if dist.is_file():
            masters = [dist]
        else:
            masters = sorted(p for p in self.root.glob("*.tex")
                             if re.search(r"^\s*\\begin\{document\}",
                                          p.read_text(encoding="utf-8",
                                                      errors="replace"), re.M))
        seen, queue = set(), list(masters)
        while queue:
            p = queue.pop()
            rp = p.resolve()
            if rp in seen or not p.is_file():
                continue
            seen.add(rp)
            text = p.read_text(encoding="utf-8", errors="replace")
            # md2tex compiles with TEXINPUTS=".:<paper root>:", so an \input
            # resolves against EITHER the file's own directory or the paper root.
            # Trying only one silently loses half the tree.
            for m in re.finditer(r"^[^%\n]*\\(?:input|include)\{([^}]+)\}",
                                 text, re.M):
                raw = m.group(1).strip()
                for base in (p.parent, self.root):
                    hit = next((c for c in (base / raw, base / (raw + ".tex"))
                                if c.is_file()), None)
                    if hit:
                        queue.append(hit)
                        break
        return seen

    def _prints(self, path):
        """Does LaTeX ever open this file? No master found means do not judge."""
        return (not self.printed) or path.resolve() in self.printed

    # A pointer that cannot resolve in the PDF is not `ok`, whatever the unit's
    # own state is. This is `_gate`'s principle, worst state wins, applied to a
    # second thing disk cannot see. It downgrades the `\ref` CHIP only, never the
    # unit CARD: a card answers "is this display built and agreed", which stays
    # true of an unwired float, while a `\ref` chip IS the claim that the pointer
    # works. Downgrading both would amber the whole set and stop informing.
    UNREACHED = ("owed", "\nBUT IT PRINTS ?? TODAY: {where} is not reached by "
                         "the master's \\input tree, so LaTeX never opens the "
                         "file that declares this label. Wire the float into a "
                         "section that the master reads, or the pointer stays "
                         "broken in the PDF however finished the display is.")

    def ref(self, label):
        """-> (state, tooltip, meta) for a `\\ref{tab:…}` / `\\ref{fig:…}`.

        Four outcomes now. The third exists because a label that resolves on
        DISK still prints `??` when nothing the master reads declares it.
        """
        u = self.by_label.get(label)
        if u is not None:
            state, tip = self._gate(u, *u.chip())
            f = u.path / "float.tex"
            # The unit lives in the workspace; the SHIPPED copy is what a section
            # inputs, so reachability is asked of the built tree when there is one.
            built = self.root / "displays" / u.path.name / "float.tex"
            target = built if built.is_file() else f
            if not self._prints(target):
                where = target.relative_to(self.root).as_posix()
                state = self.UNREACHED[0]
                tip += self.UNREACHED[1].format(where=where)
            return (state, f"\\ref{{{label}}} → {tip}", self._dmeta(u))
        where = self.labels.get(label)
        if where:
            p, line = where
            rel = p.relative_to(self.root).as_posix()
            if not self._prints(p):
                return ("owed",
                        f"\\ref{{{label}}} resolves to a \\label in {rel}:{line}, "
                        f"which the master NEVER READS, so it compiles to ??. "
                        f"A label on disk is not a label in the document.",
                        {"files": [(f"{rel}:{line}", p)]})
            return ("ok", f"\\ref{{{label}}} resolves to a \\label in {rel}:{line}, "
                          f"which is NOT a {self.disp_rel} unit. Fine for a section "
                          f"or equation label; check it if a display was meant.",
                    {"files": [(f"{rel}:{line}", p)]})
        near = difflib.get_close_matches(label, self.labels, n=3, cutoff=0.4)
        tip = (f"\\ref{{{label}}} resolves to NO \\label anywhere in this paper. "
               f"It compiles to ??")
        if near:
            tip += "\nlabels that DO exist, nearest first: " + ", ".join(near)
        return ("unowned", tip, {})

    def summary(self):
        return (f"{len(self.bib)} bib keys from "
                f"{', '.join(self.bib_files) or 'no .bib'}"
                f"{f', {len(self.refs)} rendered references' if self.refs else ''}; "
                f"{len(self.probes)} probe entries serving {len(self.by_q)} "
                f"question ids")


def _value(raw):
    """A board.md header value, without its trailing `# comment`."""
    return (raw or "").split("#", 1)[0].strip()


def load(board_dir, meta):
    """Return a Paper for a board that declares `dialect: paper`, else None."""
    if _value(meta.get("dialect")).lower() != "paper":
        return None
    root = (Path(board_dir) / (_value(meta.get("paper_root")) or "..")).resolve()
    if not root.is_dir():
        return None
    return Paper(root)
