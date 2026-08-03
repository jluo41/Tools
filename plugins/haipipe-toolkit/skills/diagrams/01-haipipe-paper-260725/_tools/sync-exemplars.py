#!/usr/bin/env python3
"""Regenerate the `📚 **Exemplars**` block in each QBv outlet page's ## Files.

The venue packs are a separate repository (`jluo41/Venue-Paper`), so an exemplar
list typed by hand goes stale the moment someone adds a PDF over there. This
reads the packs and rewrites the block between two markers, so the board's
count and the folder's count can never disagree.

    python3 _tools/sync-exemplars.py            # rewrite
    python3 _tools/sync-exemplars.py --check    # exit 1 if any page is stale

WHAT COUNTS AS AN EXEMPLAR: one PAPER, keyed by filename stem, so a `.md` and
its source `.xml` are one exemplar with two files. `INDEX.md` and `*_RESULTS.md`
are the pack's own manifests, not papers, and are listed apart from the count.
That is the difference between this number and `ls | wc -l`.

Paths are written board-relative, which is what `cli/check.py`'s dead-file-path
rule resolves and what the served board turns into a working PDF link.
"""
import argparse
import collections
import pathlib
import re
import sys

BOARD = pathlib.Path(__file__).resolve().parent.parent
VENUE = (BOARD / ".." / ".." / "paper" / "venue").resolve()
REL = "../../paper/venue"          # board-relative prefix, as Files rows want
BEGIN = "<!-- exemplars:begin -->"
END = "<!-- exemplars:end -->"
KBEGIN = "<!-- kinds:begin -->"
KEND = "<!-- kinds:end -->"
KINDS_YML = (BOARD / ".." / ".." / "paper" / "1-lifecycle" / "haipipe-paper-stage"
             / "stages" / "section-kinds.yml").resolve()
# Which kind lands in which S family. `appendix` is the only one that goes to
# Appendix and takes a LETTER unit; every other kind is a numbered Main unit.
# The families and unit shapes are haipipe-board/src/parse.py's S grammar.
APPENDIX_KINDS = {"appendix"}
# `letter` is a whole ARTICLE FORMAT, not a section of the main article: a JAMA
# research letter is a short standalone paper. Numbering it into the Main
# sequence put it AFTER the appendix, which is not a reader order at all.
STANDALONE_KINDS = {"letter"}
PAPER_SUFFIX = (".pdf", ".md", ".xml")
MANIFEST = re.compile(r"^(INDEX|.*_RESULTS)$", re.I)
# A `.md` that opens `# Exemplar: ...` is a NOTE ABOUT a paper, not the paper.
# Verified 260802: burns-2024-…md is 303 words and carries no article text, while
# schroeder-2019-…md sits beside its own .pdf and collapses onto that stem anyway.
NOTE_HEAD = re.compile(r"^#\s*Exemplar:", re.I)


def is_note(p):
    if p.suffix.lower() != ".md":
        return False
    return bool(NOTE_HEAD.match(p.read_text(encoding="utf-8", errors="replace")[:200].lstrip()))

# One QBv outlet page per venue outlet. `examples_owner` is set only when the
# exemplars do NOT sit under the outlet: the single-outlet and non-journal packs
# keep examples/ at family level, which is the group intro on the Index.
OUTLETS = [
    ("QBv1-misq.md",                   "playbook-utd-is/MISQ",                            None),
    ("QBv2-isr.md",                    "playbook-utd-is/ISR",                             None),
    ("QBv3-ms-is.md",                  "playbook-utd-is/MS-IS",                           None),
    ("QBv4-ms-marketing.md",           "playbook-utd-is/MS-Marketing",                    None),
    ("QBv5-jama.md",          "playbook-jama-portfolio/jama-flagship",           None),
    ("QBv6-jama-im.md",                "playbook-jama-portfolio/jama-im",                 None),
    ("QBv7-jama-network-open.md",           "playbook-jama-portfolio/jama-netopen",            None),
    ("QBv8-npj-digital-medicine.md",   "playbook-nature-portfolio/npj-digital-medicine",  None),
    ("QBv9-nature-medicine.md",        "playbook-nature-portfolio/nature-medicine",       None),
    ("QBv10-nature-communications.md",  "playbook-nature-portfolio/nature-communications", None),
    ("QBv11-nature-human-behaviour.md", "playbook-nature-portfolio/nature-human-behaviour", None),
    ("QBv12-nature-machine-intelligence.md",                    "playbook-nature-portfolio/NMI",                   None),
    ("QBv13-pnas.md",                   "playbook-pnas/pnas",                              "playbook-pnas"),
    ("QBv14-diabetes-care.md",          "playbook-medical-journals/diabetes-care",         None),
    ("QBv15-grant.md",                   "playbook-grant",                                  "playbook-grant"),
    ("QBv16-patent.md",                  "playbook-patent",                                 "playbook-patent"),
]

YEAR = re.compile(r"^(.+?)-((?:19|20)\d\d)(?:-|$)")


def label(stem):
    """`krebs-2018-jama-effect-of-opioid…` -> `Krebs 2018`.

    The author part keeps every hyphen segment (`mon-williams` -> `Mon-Williams`,
    `chen-w` -> `Chen-W`), because dropping one renames a real person. No label
    at all when the part carries no letters (`article2338266`): the filename is
    already on the row, and a wrong label is worse than none.
    """
    m = YEAR.match(stem)
    if not m:
        return ""
    who = m.group(1)
    if not re.search(r"[a-z]", who) or re.search(r"\d", who):
        return ""
    parts = [s[:1].upper() + s[1:] for s in who.split("-") if s]
    return f"{'-'.join(parts)} {m.group(2)}"


def kinds_for(outlet_dir):
    """The outlet's declared section kinds, read from stages/section-kinds.yml.

    This is the JOIN between this group and the paper board: section-edit runs
    per unit and writes one `S-Main-<n>` or `S-Appendix-<letter>` page per kind,
    so an outlet's kind list IS the page list a paper at that venue will have.
    Parsed with a narrow reader rather than a yaml dependency, because the
    board engine is standard-library only.
    """
    if not KINDS_YML.is_file():
        return []
    pack, outlet = outlet_dir.split("/", 1) if "/" in outlet_dir else (outlet_dir, None)
    if outlet is None:
        return []
    body = KINDS_YML.read_text(encoding="utf-8")
    body = body.split("\noutlets:", 1)[-1]
    cur = None
    for line in body.split("\n"):
        if re.match(r"^\S", line):
            break
        m = re.match(r"^  (\S+):\s*$", line)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r"^    (\S+):\s*\[(.*?)\]", line)
        if m and cur == pack and m.group(1) == outlet:
            return [k.strip() for k in m.group(2).split(",") if k.strip()]
    return []


def kinds_block(outlet_dir):
    ks = kinds_for(outlet_dir)
    out = [KBEGIN, ""]
    if not ks:
        out += ["📐 **Section kinds** · none declared in `stages/section-kinds.yml`, "
                "so this venue is blueprint-only: the S-Venue-0 blueprint is binding "
                "and no per-section pack is resolved.", "", KEND]
        return "\n".join(out)
    main = [k for k in ks if k not in APPENDIX_KINDS]
    app = [k for k in ks if k in APPENDIX_KINDS]
    out += [f"📐 **Section kinds** · {len(ks)} declared in `stages/section-kinds.yml`, "
            "regenerated by `_tools/sync-exemplars.py`", "",
            "`section-edit` runs once per kind, and writes one page each. "
            f"That is {len(main)} numbered `S-Main-<n>` page{'' if len(main)==1 else 's'}"
            + (", plus `S-Appendix-<letter>`." if app else ", and no Appendix family."), ""]
    # The unit is the READER-ORDER position, so the number is the venue's own.
    # Verified against a real paper in this repo: S-Main-0-abstract.md,
    # S-Main-1-introduction.md ... S-Main-8-conclusion.md.
    n_main, n_app = 0, 0
    for k in ks:
        if k in STANDALONE_KINDS:
            out.append(f"- `S-Main-0` of its OWN paper · {k}, a standalone article format "
                       "rather than a section of this one")
            continue
        if k in APPENDIX_KINDS:
            unit = f"S-Appendix-{chr(ord('A') + n_app)}"; n_app += 1
        else:
            unit = f"S-Main-{n_main}"; n_main += 1
        out.append(f"- `{unit}` · {k}")
    # Short sentences on purpose. The readability pass of 260802 scored this
    # block on every one of the 16 pages, and no page agent can reach it.
    out += ["",
            "A kind is the SMALLEST unit a paper gets here, not a ceiling.",
            "One kind can spread across several numbered Main pages.",
            "This repo's own MISQ paper runs to `S-Main-8-conclusion`, and the numbers above "
            "move with it.",
            "The ORDER above is the RESOLVER's, and it is not always the desk's. "
            "Nature Medicine, Nature Communications, Nature Human Behaviour, Nature "
            "Machine Intelligence and npj Digital Medicine all print Methods LAST, "
            "and PNAS reads Significance first; `section-kinds.yml` orders none of "
            "them that way (found 260803 by five venue pages at once). The page's "
            "`Venue-Structure` figure is where the DESK's printed order lives, and "
            "where the two disagree it says so."]
    out += ["", KEND]
    return "\n".join(out)


MINED = re.compile(r"Extracted from\s+(?:(\d+)\s+of\s+the\s+)?(\d+)", re.I)


def mined_base(outlet_dir):
    """How many papers the outlet's style guides were actually MINED from.

    NOT the same number as the folder count, and the gap is the point: Nature
    Medicine stores 24 papers and every `natmed-<kind>/style.md` says it was
    extracted from 14. A norm inherits the authority of the papers behind it,
    so a page may legitimately say "3 exemplars" about a guide while 16 sit on
    disk. Returns the distinct bases seen across that outlet's guides.
    """
    d = VENUE / outlet_dir
    if not d.is_dir():
        return set()
    seen = set()
    for f in sorted(d.glob("*/style.md")):
        m = MINED.search(f.read_text(encoding="utf-8", errors="replace")[:600])
        if m:
            seen.add(int(m.group(1) or m.group(2)))
    return seen


def scan(owner):
    """-> (papers, manifests, error). `papers` is stem -> [filenames]."""
    ex = VENUE / owner / "examples"
    if not ex.is_dir():
        return {}, [], f"no `examples/` folder under `{REL}/{owner}/`"
    papers, manifests = collections.defaultdict(list), []
    for p in sorted(ex.iterdir()):
        if p.suffix.lower() not in PAPER_SUFFIX or p.name.startswith("."):
            continue
        if MANIFEST.match(p.stem):
            manifests.append(p.name)
        else:
            papers[p.stem].append(p.name)
    # A stem whose ONLY file is an `# Exemplar:` note has no paper behind it.
    notes = [k for k, v in papers.items()
             if all(is_note(ex / n) for n in v)]
    for k in notes:
        manifests.append(f"{papers.pop(k)[0]}  (a note about the paper, no article text on disk)")
    return dict(papers), manifests, ""


def block_for(outlet_dir, examples_owner):
    owner = examples_owner or outlet_dir
    papers, manifests, err = scan(owner)
    n = len(papers)

    mined = mined_base(outlet_dir)
    gap = ""
    if mined:
        lo, hi = min(mined), max(mined)
        span = f"{lo}" if lo == hi else f"{lo} to {hi}"
        if hi < n:
            gap = (f" · the section guides were mined from {span} of them, "
                   f"so {n - hi} stored paper{'' if n - hi == 1 else 's'} "
                   f"back no norm")
        else:
            gap = f" · the section guides were mined from {span}"
    out = [BEGIN, "",
           f"📚 **Exemplars** · {n} paper{'' if n == 1 else 's'} on disk{gap}, "
           f"regenerated by `_tools/sync-exemplars.py`"]
    if examples_owner:
        out += ["", f"Filed at FAMILY level under `{REL}/{owner}/examples/`, "
                    f"not under the outlet (the group intro on the Index)."]
    if err:
        out += ["", f"- none. {err[0].upper()}{err[1:]}, so this outlet states "
                    "section norms with no exemplar behind them."]
    elif not papers:
        out += ["", "- none. The folder holds no paper, so this outlet states "
                    "section norms with no exemplar behind them."]
    else:
        out.append("")
        for stem in sorted(papers):
            lab = label(stem)
            names = papers[stem]
            row = f"- `{REL}/{owner}/examples/{names[0]}`"
            extra = [f"+{pathlib.Path(x).suffix.lstrip('.')}" for x in names[1:]]
            bits = [b for b in (lab, " ".join(extra)) if b]
            out.append(row + (" · " + " · ".join(bits) if bits else ""))
    if manifests:
        out += [""] + [f"- `{REL}/{owner}/examples/{m}` · the pack's own manifest, "
                       "not an exemplar" for m in manifests]
    return "\n".join(out + ["", END]), n


def apply(page, text, new):
    if BEGIN in text and END in text:
        return re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: new, text, flags=re.S)
    m = re.search(r"(?m)^## Files\n(.*?)(?=^## |\Z)", text, re.S)
    if not m:
        sys.exit(f"{page}: no ## Files section to write into")
    return text[:m.start(1)] + m.group(1).rstrip("\n") + "\n\n" + new + "\n\n" + text[m.end(1):]


def count_claims(text, allowed):
    """Every OTHER place the page states an exemplar count, and whether it agrees.

    A page that says `21 exemplars` while the folder holds 20 and no style guide
    was mined from 21 contradicts itself in one screen, which is the exact
    failure this script exists to prevent. A count that matches EITHER the
    folder or a guide's own mined base is legitimate and passes.
    """
    bad = []
    for m in re.finditer(r"(\d+)\s+exemplars?\b", text):
        if int(m.group(1)) in allowed:      # the folder count, or a real mined base
            continue
        if "paper" in text[max(0, m.start() - 40):m.start()]:
            continue                       # the generated block's own wording
        bad.append(m.group(0))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 if any page is stale")
    args = ap.parse_args()

    stale, drift, total = [], [], 0
    for name, outlet_dir, owner in OUTLETS:
        page = BOARD / "QBv-venue-packs" / name
        text = page.read_text(encoding="utf-8")
        new, n = block_for(outlet_dir, owner)
        allowed = {n} | mined_base(outlet_dir)
        total += n
        after = apply(name, text, new)
        kb = kinds_block(outlet_dir)
        if KBEGIN in after:
            after = re.sub(re.escape(KBEGIN) + r".*?" + re.escape(KEND),
                           lambda _: kb, after, flags=re.S)
        else:
            after = after.replace(END, END + "\n\n" + kb, 1)
        if after != text:
            stale.append(name)
            if not args.check:
                page.write_text(after, encoding="utf-8")
                after = page.read_text(encoding="utf-8")
        for claim in count_claims(after, allowed):
            drift.append(f"{name}: says '{claim}', folder has {n}")

    for s in stale:
        print(f"{'STALE' if args.check else '  rewrote'} {s}")
    for d in drift:
        print(f"  ⚠️ count drift · {d}")
    print(f"{'✅' if not (args.check and (stale or drift)) else '❌'} "
          f"{total} exemplars across {len(OUTLETS)} outlets · "
          f"{len(stale)} block(s) {'stale' if args.check else 'rewritten'} · "
          f"{len(drift)} count drift")
    return 1 if args.check and (stale or drift) else 0


if __name__ == "__main__":
    sys.exit(main())
