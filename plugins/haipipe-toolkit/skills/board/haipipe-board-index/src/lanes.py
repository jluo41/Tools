#!/usr/bin/env python3
"""One `⚙️ engine · 📋 pages · 📂 folder` lane block per group, in board.md.

    python3 lanes.py <board-dir>            # dry run, prints what would change
    python3 lanes.py <board-dir> --apply    # write board.md

WHAT A LANE BLOCK IS FOR (JL 260730). The board-level canvas answers "how do the
groups connect"; the index below it answers "what pages exist". Neither answers
the question a person actually opens a group to ask: for THIS page, which engine
file governs it, and which folder artifact does it produce? That mapping is one
row per page, and it lives in the group's own intro, where a group intro has
accepted a ``` figure since QC2 (JL 260724).

WHY IT ROUND-TRIPS. The page roster is generated (it must never disagree with
`## Pages`), but the engine and folder cells are JUDGEMENT, and judgement is
typed by a person. So this script reads the block back before it writes one:

    · a row whose page still exists KEEPS the engine/folder cells already there
    · a page with no row yet arrives with `?` in both, which is honest and is
      also the to-do list
    · a row whose page is gone is DROPPED, the same rule xcal.py applies to the
      frame of a retired page

That is the same bargain as `xcal.py` keeping a human's frame position: the
generator owns the skeleton, the person owns the meaning, and re-running is
therefore never destructive.

WHY IT PARSES board.md AND NOT THE ENGINE. This script deliberately does not
import haipipe-board's `src/`. A board's `## Pages` section plus each page's
`# ` title is all the input it needs, and staying at that surface means the two
skills can ship on their own clocks.
"""
import argparse
import re
import sys
from pathlib import Path

W_ENG = 26            # engine column
W_NAME = 29           # page-name column
UNSET = "?"           # not mapped yet: honest, and it reads as a to-do
HEAD = "⚙️ ENGINE"
LEFT, RIGHT = "◀──", "──▶"


# ── read ──────────────────────────────────────────────────────────────────
def groups_of(board_md):
    """`## Pages` -> [(heading, [page filename, ...]), ...] in listed order."""
    txt = board_md.split("\n## Pages\n", 1)
    if len(txt) < 2:
        return []
    pages = re.split(r"\n## \w", txt[1])[0]
    out, cur, fence = [], None, False
    for raw in pages.split("\n"):
        ln = raw.strip()
        if ln.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if ln.startswith("### "):
            cur = ln[4:].strip()
            out.append((cur, []))
        elif cur and ln.endswith(".md"):
            out[-1][1].append(ln.lstrip("-*· ").strip())
    return out


def title_of(board, name):
    """A page's own `# ` line, shortened to the name column. Never invented: an
    untitled page shows its filename stem rather than a guess."""
    hits = sorted(board.rglob(name))
    hits = [h for h in hits if "_archive" not in h.parts]
    if not hits:
        return name[:-3] if name.endswith(".md") else name
    for ln in hits[0].read_text(encoding="utf-8").split("\n"):
        if ln.startswith("# "):
            t = ln[2:].strip()
            # "Page Opening: the head and the door" -> "Opening: the head..."
            t = re.sub(r"^(Page|The)\s+", "", t)
            return t if len(t) <= W_NAME - 1 else t[:W_NAME - 2].rstrip() + "…"
    return name[:-3]


def page_id(name):
    """`QAa5-where-we-are.md` -> `QAa5`; `Skill-0-haipipe-board.md` -> `Skill-0`;
    `Q-Skill-haipipe-board.md` -> whole stem (legacy named family)."""
    stem = name[:-3] if name.endswith(".md") else name
    if re.match(r"^Q-[A-Z]", stem) or stem.startswith("S-"):
        return stem
    m = re.match(r"^((?:Skill|Agent)-\d+)-", stem)
    if m:
        return m.group(1)
    return re.split(r"-", stem, 1)[0]


def parse_block(lines):
    """An existing lane block -> {page-id: (engine_lines, name, folder)}.

    The NAME is kept too, not only the engine and folder cells. A page's `# `
    title is the SEED for a new row, but the column is 29 characters wide and a
    real title rarely fits it: "How to design the haipipe-board folder
    structure?" truncates to noise, where a person writes "the folder
    structure". So every cell in the row is human-owned once it exists, and the
    id is what carries identity: it is the id that is the link.
    """
    keep, last = {}, None
    for ln in lines:
        if LEFT in ln and RIGHT in ln:
            eng, rest = ln.split(LEFT, 1)
            mid, art = rest.split(RIGHT, 1)
            mid = mid.strip().split(None, 1)
            if not mid:
                continue
            pid = mid[0]
            name = mid[1].strip() if len(mid) > 1 else ""
            keep[pid] = ([eng.strip()] if eng.strip() else [], name, art.strip())
            last = pid
        elif last and ln.strip() and LEFT not in ln and not ln.startswith(("⚙", "─", "`")):
            keep[last][0].append(ln.strip())     # a second engine file for that row
    return keep


# ── write ─────────────────────────────────────────────────────────────────
def block(rows):
    """rows: [(engine_lines, id, name, folder)] -> the fenced figure."""
    w_id = max(len(r[1]) for r in rows) + 2      # PER GROUP: one long id in the
    mid = w_id + W_NAME                          # skill roster must not push a
    out = ["```text",                            # wide gutter into every group
           f"{HEAD:<{W_ENG}}     {'📋 PAGES · the working record':<{mid}}  📂 FOLDER",
           f"{'─' * (W_ENG - 1):<{W_ENG}}     {'─' * (mid - 2):<{mid}}  {'─' * 24}"]
    for engs, pid, name, art in rows:
        first = engs[0] if engs else UNSET
        out.append(f"{first:<{W_ENG}} {LEFT} {pid:<{w_id}}{name:<{W_NAME}} "
                   f"{RIGHT}  {art or UNSET}".rstrip())
        for extra in engs[1:]:
            out.append(extra)
    out.append("```")
    return out


def collect_kept(lines):
    """Every lane block in the file -> ONE {page-id: cells} map.

    Global, not per block, and that is the point (260730, the Design/Delivery/
    Engine/Execute regroup): when a page MOVES to another group, its row is new
    in that group's block but the person's engine/name/folder cells are not new
    knowledge. Keying by page id across the whole file means a regroup carries
    every typed cell with the page, instead of resetting it to `?`.
    """
    kept, i = {}, 0
    while i < len(lines):
        if lines[i].strip().startswith("```") and i + 1 < len(lines) \
                and HEAD in lines[i + 1]:
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            kept.update(parse_block(lines[i + 1:j]))
            i = j + 1
            continue
        i += 1
    return kept


def rewrite(board, apply):
    bp = board / "board.md"
    src = bp.read_text(encoding="utf-8")
    roster = {g: files for g, files in groups_of(src)}
    if not roster:
        sys.exit("no ## Pages section with groups: nothing to lane")

    out, group, seen, report = [], None, set(), []
    lines = src.split("\n")
    kept = collect_kept(lines)
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("### "):
            group = ln[4:].strip()
            out.append(ln)
            i += 1
            continue
        # an existing block: swallow it (its cells are already in `kept`)
        if group and ln.strip().startswith("```") and i + 1 < len(lines) \
                and HEAD in lines[i + 1]:
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            out.extend(emit(board, group, roster.get(group, []), kept, report))
            seen.add(group)
            i = j + 1
            continue
        # first .md line of a group that has no block yet -> put one in
        if group and group not in seen and ln.strip().endswith(".md") \
                and group in roster:
            if out and out[-1].strip():
                out.append("")
            out.extend(emit(board, group, roster[group], kept, report))
            seen.add(group)
        out.append(ln)
        i += 1

    new = "\n".join(out)
    # dropped is judged against the WHOLE roster, not one group's: after a
    # regroup a page has merely moved, and only a page in no group is gone.
    live = {page_id(n) for files in roster.values() for n in files}
    gone = sorted(p for p in kept if p not in live)
    if gone:
        report.append(f"dropped (page in no group): {', '.join(gone)}")
    for line in report:
        print(line)
    if new == src:
        print("· board.md already current")
        return
    if not apply:
        print(f"\n(dry run) {bp} would change; pass --apply to write it")
        return
    bp.write_text(new, encoding="utf-8")
    print(f"\n✅ {bp} rewritten · rebuild the board to see it")


def emit(board, group, files, kept, report):
    rows, added = [], []
    for name in files:
        pid = page_id(name)
        engs, label, art = kept.get(pid, ([], "", ""))
        if pid not in kept:
            added.append(pid)
            label = title_of(board, name)        # seed only; a person may reword it
        rows.append((engs, pid, label, art))
    if not rows:
        return []
    tok = group.split("·", 1)[0].strip()
    note = f"{tok:<9} {len(rows)} row(s)"
    if added:
        note += f" · new (mapped as {UNSET}): {', '.join(added)}"
    report.append(note)
    return block(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("board", help="the board folder")
    ap.add_argument("--apply", action="store_true", help="write board.md")
    a = ap.parse_args()
    b = Path(a.board)
    if not (b / "board.md").is_file():
        sys.exit(f"not a board folder (no board.md): {b}")
    rewrite(b, a.apply)


if __name__ == "__main__":
    main()
