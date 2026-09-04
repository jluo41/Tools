#!/usr/bin/env python3
"""Resolve a Section Page's `structure-source` against its bound QBv Venue Page.

The contract's one job is to say WHERE a Section's move structure comes from,
and until 0.5.0 it said it in prose naming a division ("Unit Guidance") that
exists on none of the 17 QBv pages. Every Section therefore resolved to
nothing and silently took the generic fallback. A prose address cannot be
wrong out loud; this can.

    resolve-structure.py <QBv page>.md <section page>.md
    resolve-structure.py <QBv page>.md --all <desk group dir>

Prints one row per Page: its `section_kind`, the relation, and the address to
write into `structure-source`. Exit 1 if any Page is MISSING (the desk owes a
division it has not written); ABSENT BY DESIGN and the fallback are legal
outcomes and exit 0.
"""
import argparse, re, sys
from pathlib import Path

# Two of the nine differ from their kind by more than capitalization, so the
# token is READ from this table and never derived from the string.
KIND2TOK = {
    "abstract":          "sec-0-abstract",
    "introduction":      "sec-1-introduction",
    "literature-review": "sec-2-related-work",
    "theory":            "sec-2-theory",
    "methods":           "sec-3-methods",
    "results":           "sec-4-results",
    "discussion":        "sec-5-discussion",
    "conclusion":        "sec-6-conclusion",
    "appendix":          "sec-a-appendix",
}
# A desk that publishes no such unit at all. The paper may still keep the
# section as a deliberate deviation a person ruled, and raising a QBv gap
# would tell a consumer-neutral asset to invent a division to suit one paper.
ABSENT_BY_DESIGN = {("qbv1-misq", "literature-review"),
                    # JAMA IM folds Conclusions into Discussion; the paper keeps a
                    # Conclusions page by the Narrative's allocation (NA01 §5.6)
                    ("qbv6-jama-im", "conclusions")}

# `### 4 · Sec-0-Abstract: one unstructured paragraph, question forward`
DIV = re.compile(r"^### (\d+) · (Sec-[0-9A-Za-z-]+):", re.M)


def divisions(qbv: Path) -> dict[str, str]:
    t = qbv.read_text(encoding="utf-8", errors="replace")
    return {m.group(2).lower(): f"{qbv.stem} §{m.group(1)} {m.group(2)}"
            for m in DIV.finditer(t)}


def kind_of(page: Path) -> str | None:
    m = re.search(r"^section_kind:\s*(\S+)", page.read_text(
        encoding="utf-8", errors="replace"), re.M)
    return m.group(1).strip() if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("qbv", type=Path)
    ap.add_argument("target", type=Path)
    ap.add_argument("--all", action="store_true",
                    help="target is a desk group dir, not one page")
    ap.add_argument("--write", action="store_true",
                    help="stamp `structure-source:` (the QBv FILE, skills-root relative) and "
                         "`structure-division:` (the row) into each Section page's header")
    ap.add_argument("--skip", default="", help="comma-separated page stems to leave untouched")
    a = ap.parse_args()

    divs = divisions(a.qbv)
    if not divs:
        print(f"⚠️  {a.qbv.stem} carries NO `Sec-` divisions. `mode: resolved` "
              f"is aspirational for this desk: every Section takes the "
              f"fallback and the gap is real.", file=sys.stderr)

    pages = (sorted(p / f"{p.name}.md" for p in a.target.iterdir() if p.is_dir())
             if a.all else [a.target])
    # A desk group also holds the desk's RD Round pages; only Sections have a
    # structure to resolve.
    pages = [p for p in pages if p.exists() and re.search(
        r"^page-type:\s*section\b", p.read_text(encoding="utf-8", errors="replace"), re.M)]
    if not pages:
        print("no Section Page found under that target", file=sys.stderr)
        return 1

    kinds: dict[str, list[Path]] = {}
    for p in pages:
        k = kind_of(p)
        if k:
            kinds.setdefault(k, []).append(p)

    rows, missing = [], 0
    for p in pages:
        k = kind_of(p)
        if not k:
            rows.append((p.stem, "(no section_kind)", "DEFECT",
                         "declare section_kind first"))
            missing += 1
            continue
        tok = KIND2TOK.get(k)
        hit = divs.get(tok) if tok else None
        if hit is None:
            # The table is MISQ-numbered (`sec-3-methods`); another desk numbers
            # the same unit differently (`Sec-2-Methods` at JAMA IM). A unique
            # `sec-<x>-<kind>` suffix hit is the same unit; two hits stay a gap.
            cands = [d for d in divs if re.fullmatch(rf"sec-[0-9a-z]+-{re.escape(k.rstrip('s'))}s?", d)]
            if len(cands) == 1:
                hit = divs[cands[0]]
        if hit:
            rel = "SHARED" if len(kinds[k]) > 1 else "EXACT"
            addr = hit + (f" · split with {len(kinds[k]) - 1} sibling Page(s)"
                          if rel == "SHARED" else "")
        elif (a.qbv.stem.lower(), k) in ABSENT_BY_DESIGN:
            rel, addr = "ABSENT BY DESIGN", "ref/generic-template.md · record the deviation on the Narrative"
        else:
            rel, addr = "MISSING", "ref/generic-template.md · raise the gap on the QBv page"
            missing += 1
        rows.append((p.stem, k, rel, addr))
        if a.write and p.stem not in {x.strip() for x in a.skip.split(",") if x.strip()}:
            skills_root = a.qbv.resolve()
            while skills_root.name != "skills" and skills_root.parent != skills_root:
                skills_root = skills_root.parent
            src_file = (a.qbv.resolve().relative_to(skills_root).as_posix() if hit
                        else "paper/workflow-phases/haipipe-paper-section/ref/generic-template.md")
            division = (hit.split(" ", 1)[1] + (" · shared with %d sibling Page(s)" % (len(kinds[k]) - 1) if rel == "SHARED" else "")
                        if hit else rel)
            txt = p.read_text(encoding="utf-8", errors="replace")
            txt = re.sub(r"(?m)^structure-(source|division):.*\n", "", txt)
            txt = re.sub(r"(?m)^(section_kind:[^\n]*\n)",
                         lambda m: m.group(1) + f"structure-source: {src_file}\nstructure-division: {division}\n", txt, count=1)
            p.write_text(txt, encoding="utf-8")

    w1 = max((len(r[0]) for r in rows), default=4)
    w2 = max((len(r[1]) for r in rows), default=12)
    print(f"{'page':<{w1}}  {'section_kind':<{w2}}  {'relation':<16}  structure-source")
    print("-" * (w1 + w2 + 20 + 40))
    for r in rows:
        print(f"{r[0]:<{w1}}  {r[1]:<{w2}}  {r[2]:<16}  {r[3]}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
