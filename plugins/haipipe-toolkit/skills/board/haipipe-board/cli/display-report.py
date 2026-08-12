#!/usr/bin/env python3
r"""Write the display-to-section map into the TOP of S-Display-Dash.md.

WHAT IT ANSWERS, per unit, in one place: what the display is called, what LaTeX
calls it, which section sentence points at it, and whether that pointer actually
resolves in the compiled PDF.

WHY GENERATED AND NEVER AUTHORED. Every column here already exists somewhere on
disk, so restating them by hand would create a third place claiming to know the
truth. This repo has been burned by that shape three times: `STATUS.md` was
retired on 2026-07-26 for holding a frontier that could only go stale; the
260727 renumber damaged its own mapping table badly enough that the rule got
written down; and `S-Main-6-results.md`'s hand-written LABEL COLLISION lane still
names `displays/Table/table-main-regression.tex`, a path that has not existed
since the folder moved.

WHERE EACH COLUMN COMES FROM
  display        the workspace folder name, which is also its page name
  latex          the \label{} inside that unit's own float.tex
  section        the S-Main page whose ## Content prose writes \ref{<label>}
  Pn.Sn          that sentence's position, counted by section-stats.py's rules:
                 #### Pn opens a paragraph, the (…) line under it is the job and
                 not prose, a > line is an apparatus lane and not prose, and one
                 source line is one sentence
  \input in      the sections/*.tex that inputs the float, if any
  prints         whether the master's own \input tree reaches that float, which
                 is a different question from whether the display is finished

    python3 <skill>/cli/display-report.py <stage-dir>           write the block
    python3 <skill>/cli/display-report.py <stage-dir> --check   non-zero if stale

The stage directory defaults to the working directory. `src/display_unit.py` holds the
anchor rules and says why they are arguments rather than `__file__`.
"""
import pathlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import display_unit as _stage                            # noqa: E402

# These were once spelled out as `3-display` and `4-main`, folders that had been
# renamed to `S05-display` and `S06-main`. Two of them were assembled from
# parts, so a grep for the joined path could not see them and they sat here
# until the script was actually RUN. Nothing is spelled out now: the stage comes
# in on the command line and everything else is found from it.
STAGE = _stage.stage_dir()
ROOT = _stage.paper_root(STAGE)
WS = _stage.authoring_dir(STAGE)
OUT = ROOT / "displays"
DASH = next(iter(sorted(STAGE.glob("*-Dash.md"))), STAGE / "S-Display-Dash.md")
SECTION_PAGES = _stage.section_pages(STAGE)

def _state(unit):
    """The unit's OWN page `state:` line, verbatim.

    Read from `<unit>.md`, which the workspace rename made a direct lookup: the
    folder and its page share one name. Quoted rather than summarised, so this
    table can never present a display as more settled than its page says it is.
    """
    page = STAGE / f"{unit}.md"
    if not page.is_file():
        return "(no page)"
    m = re.search(r"^state:\s*(.+)$",
                  page.read_text(encoding="utf-8", errors="replace")[:1200], re.M)
    return m.group(1).strip() if m else "(no state: line)"


def _short(unit):
    """`S-Display-1a-hero-concept` -> `01a`, the id a human says out loud."""
    m = re.match(r"S-Display-(\d+)([a-z0-9]*)-", unit)
    return f"{int(m.group(1)):02d}{m.group(2)}" if m else unit


def _used(where):
    r"""Every place that points at one display, on ONE line.

    One row is one display, so a unit bound from two sentences folds them into a
    single cell rather than spilling into a continuation row. The section number
    repeats only when it changes: `§4 P0.S6, P3.S5` reads as two sentences in §4.
    """
    if not where:
        return "(nothing points here)"
    out, last = [], None
    for page, pn, sn in where:
        m = re.match(r"S-Main-(\w+)-", page)
        sec = m.group(1) if m else page
        out.append(f"P{pn}.S{sn}" if sec == last else f"§{sec} P{pn}.S{sn}")
        last = sec
    return ", ".join(out)


BEGIN = "<!-- display-report:begin (generated) -->"
END = "<!-- display-report:end -->"
REF = re.compile(r"\\(?:auto|C|c)?ref\{((?:tab|fig):[^}]*)\}")


def master_closure():
    r"""Every .tex LaTeX opens, from the master this paper actually SHIPS.

    WHICH MASTER. `3-dist/tex/paper.tex` is the live deliverable: `md2tex.py`
    generates `3-dist/tex/S-Main-*.tex` one-way from the S-Main pages, and
    `paper.tex` inputs those. The root `*.tex` with its hand-written `sections/`
    tree is the LEGACY one, kept building but no longer fed by the .md prose.
    Measuring the legacy tree reported `no` for displays that have been in the
    shipped PDF all along, which is the correction this function exists to make
    (JL 2026-07-28, option A: one live deliverable, one honest column).

    PATH RESOLUTION. `md2tex.py` compiles with `TEXINPUTS=".:<paper root>:"`, so
    an `\input` inside `3-dist/tex/` resolves against EITHER its own directory or
    the paper root. `\input{S-Main-3-theory}` takes the first and
    `\input{displays/S-Display-1a-hero-concept/float}` the second, so a walker
    that tries only one of them silently loses half the tree.
    """
    dist = ROOT / "3-dist" / "tex" / "paper.tex"
    if dist.is_file():
        queue = [dist]
    else:
        queue = [p for p in sorted(ROOT.glob("*.tex"))
                 if re.search(r"^\s*\\begin\{document\}",
                              p.read_text(encoding="utf-8", errors="replace"), re.M)]
    seen = set()
    while queue:
        p = queue.pop()
        if not p.is_file() or p.resolve() in seen:
            continue
        seen.add(p.resolve())
        for m in re.finditer(r"^[^%\n]*\\(?:input|include)\{([^}]+)\}",
                             p.read_text(encoding="utf-8", errors="replace"), re.M):
            raw = m.group(1).strip()
            for base in (p.parent, ROOT):
                hit = next((c for c in (base / raw, base / (raw + ".tex"))
                            if c.is_file()), None)
                if hit:
                    queue.append(hit)
                    break
    return seen


def master_name():
    d = ROOT / "3-dist" / "tex" / "paper.tex"
    return "3-dist/tex/paper.tex" if d.is_file() else "the root master"


def sentences(page):
    """-> [(Pn, Sn, text)] over a S-page's ## Content, by section-stats' rules."""
    text = page.read_text(encoding="utf-8", errors="replace")
    if "## Content" not in text:
        return []
    body = text.split("## Content", 1)[1]
    for stop in ("## Items to Finish", "## Where we are", "## Files", "## Log"):
        if stop in body:
            body = body.split(stop, 1)[0]
    out, para, n, job_seen = [], None, 0, False
    for raw in body.split("\n"):
        s = raw.strip()
        if s.startswith("#### ") and re.match(r"P\d+\.", s[5:].strip()):
            para = re.match(r"P(\d+)\.", s[5:].strip()).group(1)
            n, job_seen = 0, False
        elif s.startswith(("#### ", "### ")):
            para = None
        elif s.startswith("(") and para and not job_seen and not n:
            job_seen = True                       # the paragraph's job, not prose
        elif not s or s.startswith((">", "```", "- ", "* ", "#", "|", "$")):
            continue
        elif para:
            n += 1
            out.append((int(para), n, s))
    return out


def collect():
    printed = master_closure()
    # where every \ref lives, by label -> [(section page, Pn, Sn)]
    cites = {}
    for page in SECTION_PAGES:
        if "_archive" in page.parts:
            continue
        for pn, sn, line in sentences(page):
            for lab in REF.findall(line):
                cites.setdefault(lab, []).append((page.stem, pn, sn))
    # a \ref written straight into the tex tree the master compiles. Distinct
    # from the S-Main scan above: that is the AUTHORED prose, this is what LaTeX
    # actually reads, and the two disagree while the tex sync lags.
    texrefs = {}
    for f in sorted(printed):
        for m in REF.finditer(re.sub(r"(?<!\\)%.*$", "",
                                     pathlib.Path(f).read_text(errors="replace"),
                                     flags=re.M)):
            texrefs.setdefault(m.group(1), set()).add(
                pathlib.Path(f).relative_to(ROOT).as_posix())

    # which sections/*.tex inputs each unit float
    inputs = {}
    for tex in sorted((ROOT / "sections").glob("*.tex")) + \
            sorted((ROOT / "appendices").glob("*.tex")):
        for m in re.finditer(r"^[^%\n]*\\input\{displays/([^/}]+)/float",
                             tex.read_text(encoding="utf-8", errors="replace"), re.M):
            inputs.setdefault(m.group(1), []).append(tex.name)

    rows = []
    # `_stage.units()` and not a `S-Display-*` glob: the prefix is one paper's
    # page-naming convention, while `float.tex` is what actually makes a folder
    # a unit. The glob returned zero on a specimen stage, and zero units made
    # the column-width computation raise on an empty sequence.
    for u in _stage.units(WS):
        ft = (u / "float.tex").read_text(encoding="utf-8")
        kind = (re.search(r"\\begin\{(table|figure)\*?\}", ft) or [None, "?"])[1]
        lab = (re.search(r"\\label\{([^}]*)\}", ft) or [None, ""])[1]
        where = cites.get(lab, [])
        rows.append({
            "unit": u.name,
            "kind": "tab" if kind == "table" else "fig",
            "label": lab,
            "where": where,
            "input": inputs.get(u.name, []),
            "prints": (OUT / u.name / "float.tex").resolve() in printed,
            "state": _state(u.name),
        })
    return rows, cites, texrefs


def block():
    rows, cites, texrefs = collect()
    wu = max(len(r["unit"]) for r in rows)
    wl = max(len(r["label"] or "-") for r in rows)
    wa = max([len(_used(r["where"])) for r in rows] + [22])
    wi = max([len(_short(r["unit"])) for r in rows] + [2])
    L = [BEGIN,
         "```",
         "DISPLAY -> SECTION MAP.  Generated by board/haipipe-board/cli/display-report.py.",
         "Do not hand-edit. Every column is read off disk: the unit is its folder name,",
         "which is also its page name; the latex name is the \\label{} in its own float.tex;",
         "the section and Pn.Sn are where a S-Main ## Content sentence writes \\ref{} to it,",
         "counted by section-stats.py's rules.",
         "",
         f"in PDF? asks the only question that matters to a reader: does this table or figure",
         f"appear in the SHIPPED document, {master_name()}, which md2tex.py generates",
         "one-way from the S-Main pages. `no · ??` means it does not and the sentence that",
         "mentions it prints ?? instead. That is NOT the same question as whether it is done:",
         "each unit's own page carries its `state:` line, and this table does not copy it.",
         "",
         f"{'id':<{wi}} {'display (unit = page)':<{wu}}  knd  {'latex name':<{wl}}  "
         f"{'used at  Pn.Sn':<{wa}}  {'in PDF?':<8}",
         f"{'-' * wi} {'-' * wu}  ---  {'-' * wl}  {'-' * wa}  {'-' * 8}"]
    for r in rows:
        L.append(f"{_short(r['unit']):<{wi}} {r['unit']:<{wu}}  {r['kind']:<3}  "
                 f"{r['label'] or '-':<{wl}}  {_used(r['where']):<{wa}}  "
                 f"{'yes' if r['prints'] else 'no · ??':<8}".rstrip())
    L += ["", "\\input that puts a float in the document:"]
    for r in rows:
        if r["input"]:
            L.append(f"  {r['unit']:<{wu}}  <- sections/{', '.join(r['input'])}")
    missing = [r for r in rows if r["where"] and not r["prints"]]
    if missing:
        L += ["",
              "OWED, and each is ONE \\input line beside a \\ref a section already writes:"]
        for r in missing:
            L.append(f"  {_short(r['unit']):<{wi}} {r['label']:<{wl}}  "
                     f"{_used(r['where'])} writes the \\ref and it prints ??")
    owned = {r["label"] for r in rows if r["label"]}
    declared = set()
    for f in ROOT.rglob("*.tex"):
        if {"_archive", ".claude"} & set(f.parts):
            continue
        declared |= set(re.findall(r"\\label\{((?:tab|fig):[^}]*)\}",
                                   f.read_text(errors="replace")))
    stray = sorted(set(cites) - owned) 
    if stray:
        L += ["", "AUTHORED PROSE POINTING AT NO UNIT (a S-Main sentence writes this \\ref):"]
        for l in stray:
            L.append(f"  {l:<{wl}}  {_used([cites[l][0]])}"
                     + ("" if l in declared else "   and NO \\label declares it anywhere"))
    orphan = sorted(l for l in texrefs if l not in owned)
    if orphan:
        L += ["", "COMPILED TEX POINTING AT NO UNIT (LaTeX reads this \\ref today):"]
        for l in orphan:
            L.append(f"  {l:<{wl}}  {', '.join(sorted(texrefs[l]))[:52]}"
                     + ("" if l in declared else "   -> ??"))
    L += ["```", END]
    return "\n".join(L)


def main():
    if not DASH.is_file():
        # A stage with no dash page is legal: `-Dash` is a control page, not a
        # page TYPE, and a small stage may not have one. Printing the block and
        # saying where it would go beats a traceback, and it still exercises
        # every line of the computation above.
        print(block())
        print(f"\n(no dash page in {STAGE.name}/, so the block above was not "
              f"written anywhere. Create `<name>-Dash.md` to give it a home.)")
        return 0
    text = DASH.read_text(encoding="utf-8")
    new = block()
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        out = head + new + rest.split(END, 1)[1]
    else:
        # Lives in ## Diagram: this IS a diagram of the set, and the two that
        # precede it are conceptual (reader order, then the id grammar) while
        # this one is where every unit actually stands.
        marker = "\n## Content"
        out = text.replace(marker, "\n[3/3] Where each display stands\n\n"
                           + new + "\n" + marker, 1)
    if "--check" in sys.argv:
        if out != text:
            print("❌ STALE: the display report on S-Display-Dash.md is out of date.")
            return 1
        print("✅ S-Display-Dash.md's display report matches disk.")
        return 0
    DASH.write_text(out, encoding="utf-8")
    print(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
