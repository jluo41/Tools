#!/usr/bin/env python3
"""Generate one paper's .bib from the shared bank, and report what does not bind.

    python3 <skill>/cli/bib-from-bank.py <stage-dir>            write the .bib
    python3 <skill>/cli/bib-from-bank.py <stage-dir> --check    report only, exit 1 if broken
    python3 <skill>/cli/bib-from-bank.py <stage-dir> --json     the same data, machine readable

It takes the STAGE and finds the paper root from it, the same way the display
tools do, because a specimen stage carries its own root under `_fixture/`.

THE SHAPE, which is QA-bank / QA-probe applied to references:

    bank.bib            venue/literature/, shared, hand-maintained, one copy
        |
        |  a literature page CLAIMS a key  ·  the manuscript \\cite{}s it
        v
    <paper>.bib         GENERATED, only the keys this paper actually uses

A literature page claims a key with the line shape the real pages already use,
under `### Sources already named`:

    - \\citep{gray2021clinical} · physician identity is among the strongest
      predictors of prescribing intensity, even after patient characteristics.

That shape was not invented here. All four literature pages on the live MISQ
paper already write it, 37 lines of 37 compliant, and nothing read them. The
`·` and the sentence after it are the point: claiming a key means saying what
job it does, which is the one thing a bare list cannot carry.

THREE FINDINGS, and only the first is an error:

    broken      used somewhere and absent from the bank. The citation will not
                resolve. Add it to the bank.
    unclaimed   cited by the manuscript and claimed by no literature page. Not
                a build failure; it means a citation nobody is answerable for.
    unused      claimed by a page and cited nowhere yet. Normal while drafting.

Stock in the bank that this paper touches at all is not reported: an entry read
and not yet needed is stock, not garbage.
"""
import json
import pathlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import display_unit as _stage                            # noqa: E402

BANK = ("Tools/plugins/haipipe-toolkit/skills/paper/venue/literature/bank.bib")
LIT_PAGE = re.compile(r"(?m)^(?:route:\s*outward|page-type:\s*literature)\s*$")
ENTRY = re.compile(r"(^@[a-zA-Z]+\s*\{\s*([^,\s]+)\s*,)", re.M)
CLAIM = re.compile(r"^-\s*\\cite[a-z]*\{([^}]*)\}\s*·\s*(\S.*)$", re.M)
CITE = re.compile(r"\\cite[a-z]*\s*(?:\[[^\]]*\])*\s*\{([^}]*)\}")
SECTION = "### Sources already named"


def entries(text):
    """-> {key: body}, brace-matched from the entry's OWN opening brace.

    Starting the scan after that brace makes the first `}` of the first field
    look like the end of the entry, which truncates every record to one field.
    It happened, and the check that should have caught it used this same
    function on both sides and agreed with itself.
    """
    out = {}
    for m in ENTRY.finditer(text):
        start, depth = m.start() + m.group(1).index("{"), 0
        for j in range(start, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    out[m.group(2)] = text[m.start():j + 1]
                    break
    return out


def keys_in(group):
    return [k.strip() for k in group.split(",") if k.strip()
            and k.strip().upper() != "TOADD"]


def literature_pages(stage):
    """Every LITERATURE page, found the way the board resolves the type.

    Not `glob("0-lifecycle/*/S-Literature-*.md")`, which was one paper's folder
    layout and one paper's filename convention. The rule underneath both is the
    head key: `route: outward` resolves a literature page (base resolution step
    2), with `page-type: literature` accepted too. Matching filenames alone drops
    any page not named for that convention, which is every specimen; matching the
    key alone would drop nothing, but the filename is kept as a cheap fallback.

    Nearest first and stop at the first folder that yields anything, so a stage
    holding its own literature pages never reaches out to its siblings.
    """
    def found_in(d):
        return [f for f in sorted(d.glob("*.md"))
                if f.name.startswith("S-Literature-")
                or LIT_PAGE.search(f.read_text(errors="ignore")[:1200])]
    here = found_in(stage)
    if here:
        return here
    for d in sorted(p for p in stage.parent.iterdir() if p.is_dir()):
        if d != stage and (out := found_in(d)):
            return out
    return []


def claimed(pages):
    """-> {key: (page, why)} from every literature page's claim lines."""
    out = {}
    for f in pages:
        text = f.read_text(errors="ignore")
        if SECTION not in text:
            continue
        block = text.split(SECTION, 1)[1].split("\n### ", 1)[0]
        for group, why in CLAIM.findall(block):
            for k in keys_in(group):
                out.setdefault(k, (f.name, why.strip()))
    return out, len(pages)


def cited(paper):
    """-> {key: [file, ...]} from the manuscript's own .tex."""
    out = {}
    files = [p for d in ("sections", "appendices") for p in paper.glob(f"{d}/*.tex")]
    for p in files:
        for group in CITE.findall(p.read_text(errors="ignore")):
            for k in keys_in(group):
                out.setdefault(k, []).append(p.name)
    return out, len(files)


def report(paper, root, stage):
    bank = entries((root / BANK).read_text(errors="ignore"))
    cl, npages = claimed(literature_pages(stage))
    ci, ntex = cited(paper)
    used = set(cl) | set(ci)
    return dict(
        bank=len(bank), pages=npages, tex=ntex,
        claimed=sorted(cl), cited=sorted(ci),
        broken=sorted(used - set(bank)),
        unclaimed=sorted(set(ci) - set(cl)),
        unused=sorted(set(cl) - set(ci)),
        write=sorted(used & set(bank)),
    ), bank, cl


def out_path(paper):
    """The .bib this paper already uses, else the one its master \\bibliography names.

    Falling back to the FOLDER name is wrong when the folder is not the paper:
    a specimen root is called `_fixture/`, so a first run wrote `_fixture.bib`
    while the master said `\\bibliography{QBt-page-types}` and BibTeX found
    nothing. The master is the authority on its own bibliography's name.
    """
    have = sorted(p for p in paper.glob("*.bib"))
    if have:
        return have[0]
    for tex in sorted(paper.glob("*.tex")):
        m = re.search(r"\\bibliography\{([^}]+)\}",
                      tex.read_text(errors="ignore"))
        if m:
            return paper / f"{m.group(1).split(',')[0].strip()}.bib"
    return paper / f"{paper.name}.bib"


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    stage = _stage.stage_dir()
    paper = _stage.paper_root(stage)
    root = next((p for p in paper.parents if (p / BANK).exists()), None)
    if root is None:
        sys.exit(f"no bank above {paper}: expected {BANK}")
    r, bank, cl = report(paper, root, stage)

    if "--json" in sys.argv:
        print(json.dumps(r, indent=2))
        sys.exit(1 if r["broken"] else 0)

    print(f"  bank {r['bank']} entries · read {r['pages']} literature page(s) "
          f"and {r['tex']} .tex file(s)")
    print(f"  claimed by a page  {len(r['claimed']):>4}")
    print(f"  cited by the paper {len(r['cited']):>4}")
    print(f"  would write        {len(r['write']):>4}")
    for tag, rows, note in (
            ("BROKEN   ", r["broken"], "used and not in the bank; add it there"),
            ("unclaimed", r["unclaimed"], "cited, and no literature page answers for it"),
            ("unused   ", r["unused"], "claimed, not cited yet")):
        if rows:
            print(f"\n  {tag} {len(rows):>4}  {note}")
            for k in rows[:12]:
                print(f"      {k}")
            if len(rows) > 12:
                print(f"      ... and {len(rows) - 12} more")

    if "--check" in sys.argv:
        sys.exit(1 if r["broken"] else 0)

    dest = out_path(paper)
    head = [
        f"%% GENERATED by paper/bib-from-bank.py from {BANK}",
        "%% Do not edit. Add an entry to the bank; claim it on a literature",
        "%% page under `### Sources already named` as",
        "%%     - \\citep{key} · what job this source does",
        f"%% {len(r['write'])} entries: claimed by a page or cited by the manuscript.",
        "",
    ]
    body = []
    for k in sorted(r["write"], key=str.lower):
        page, why = cl.get(k, ("", ""))
        if page:
            body.append(f"%% claimed by {page} · {why[:110]}")
        body.append(bank[k].strip())
        body.append("")
    dest.write_text("\n".join(head + body), encoding="utf-8")
    print(f"\n  wrote {dest.name} ({len(r['write'])} entries)")
    sys.exit(1 if r["broken"] else 0)
