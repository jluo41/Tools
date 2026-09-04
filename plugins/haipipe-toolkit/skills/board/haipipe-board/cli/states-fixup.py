#!/usr/bin/env python3
"""Second pass after states-merge.py: a tick row that landed in the merged Discussion
block (because its old States group was a `####` heading, or any other shape the first
pass filed as a thread) moves onto its Aim when that Aim is on the page and still has
no `**Now:**` line. A heading left with nothing under it goes; an emptied merged block
goes with its heading. Verbatim rule as before: nothing is dropped that is not moved.

Usage: states-fixup.py [--write] <page.md>...
"""
import importlib.util, re, sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("sm", Path(__file__).with_name("states-merge.py"))
sm = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(sm)
MERGED_H = "### From the retired States section"

def aim_blocks(aims_body):
    """[(start, end, aid)] for each Aim row and its indented continuation."""
    out, i = [], 0
    while i < len(aims_body):
        m = sm.AIM_ROW.match(aims_body[i])
        if not m:
            i += 1; continue
        j = i + 1
        while j < len(aims_body) and (aims_body[j].startswith("  ") or (not aims_body[j].strip() and j + 1 < len(aims_body) and aims_body[j + 1].startswith("  "))):
            j += 1
        out.append((i, j, m.group(1))); i = j
    return out

def fixup(text):
    lines = text.split("\n")
    secs = sm.sections(lines)
    names = [h.strip() if h else None for h, _ in secs]
    if "## Discussion" not in names or "## Aims" not in names:
        return None, "no Discussion or no Aims"
    di, ai = names.index("## Discussion"), names.index("## Aims")
    disc = secs[di][1]
    start = next((i for i, l in enumerate(disc) if l.startswith(MERGED_H)), None)
    if start is None:
        return None, "no merged block"
    keep, block = disc[:start], disc[start + 1:]
    aims_body = list(secs[ai][1])
    blocks = aim_blocks(aims_body)
    has_now = {aid: any(aims_body[k].startswith("  **Now:**") for k in range(s, e)) for s, e, aid in blocks}
    moved, rest = {}, []
    for r in sm.rows(block):
        m = sm.TICK_ROW.match(r[0])
        if m and m.group(2) in has_now and not has_now[m.group(2)]:
            moved.setdefault(m.group(2), []).append((m.group(1), m.group(3).strip(), r[1:]))
        else:
            rest.extend(r)
    if not moved:
        return None, "nothing to move"
    # apply onto Aims, last block first so indices stay valid
    for s, e, aid in reversed(blocks):
        if aid not in moved: continue
        emoji = moved[aid][0][0]
        row = aims_body[s]
        if not re.match(rf"^- {sm.TICK}\s", row):
            aims_body[s] = re.sub(r"^- ", f"- {emoji} ", row, count=1)
        now_lines = []
        for _e, fact, cont in moved[aid]:
            now_lines.append(f"  **Now:** {fact}"); now_lines.extend(cont)
        k = next((x for x in range(s, e) if "**Done when:**" in aims_body[x]), None)
        if k is not None:
            k += 1
            while k < e and aims_body[k].startswith("  ") and not re.match(r"^  \*\*\w", aims_body[k]): k += 1
            aims_body[k:k] = now_lines
        else:
            end = e
            while end > s and not aims_body[end - 1].strip(): end -= 1
            aims_body[end:end] = now_lines
    secs[ai] = (secs[ai][0], aims_body)
    # prune headings that now cover nothing
    pruned = []
    for i, l in enumerate(rest):
        if l.startswith("#"):
            nxt = next((x for x in rest[i + 1:] if x.strip()), None)
            if nxt is None or nxt.startswith("#"):
                continue
        pruned.append(l)
    while pruned and not pruned[-1].strip(): pruned.pop()
    if any(x.strip() for x in pruned):
        disc = keep + [MERGED_H + " (merged 260831)"] + pruned + [""]
    else:
        disc = keep
        while disc and not disc[-1].strip(): disc.pop()
        disc.append("")
    secs[di] = (secs[di][0], disc)
    out = []
    for h, b in secs:
        if h is not None: out.append(h)
        out.extend(b)
    # drop an emptied Discussion section entirely? keep it: the section existed before the merge or was created by it;
    # an empty `## Discussion` renders as "Discussion (0)", which the renderer already shows for pages without threads.
    new_text = "\n".join(out)
    old_norm = {sm.norm(l) for l in block if l.strip() and not l.startswith("#")}
    new_norm = {sm.norm(l) for l in out}
    lost = [l for l in old_norm if l and l not in new_norm]
    return new_text, dict(moved=sorted(moved), block_gone=not any(x.strip() for x in pruned), lost=lost)

def main():
    args = sys.argv[1:]; write = "--write" in args
    paths = [Path(a) for a in args if a.endswith(".md")]
    touched = 0
    for p in paths:
        new, st = fixup(p.read_text(encoding="utf-8"))
        if new is None: continue
        flag = "LOST " if st["lost"] else "ok   "
        print(f"{flag}{p.name}: moved {st['moved']} · merged block {'removed' if st['block_gone'] else 'kept'}")
        for l in st["lost"][:3]: print("      lost:", l[:110])
        if write and not st["lost"]:
            p.write_text(new, encoding="utf-8"); touched += 1
    if write: print(f"written {touched}")

if __name__ == "__main__":
    main()
