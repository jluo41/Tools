#!/usr/bin/env python3
"""Fold an Aim group numbered past the page's Content divisions into `### P · Page-level`.

Rule (JL 260831, QPf12 row 2 "should map to the content", and the fold ruling of the
same night): `A<n>` is the n-th direct `###` division of Content; a group with no n-th
division is page-level by construction, so its rows become `P<k>` ids under
`### P · Page-level`. The id is renamed together in the page, the LATEST plan (rows and
🎯 marks) and the live record files in outline/ (discussion, log, feedback, evidence,
requirement, files); older plan versions are frozen history and are left alone.
One dated record lands in <stem>-log.md. Nothing is deleted: every moved row's text
must reappear verbatim or the page is not written.

Usage: aims-fold-to-p.py [--write] <board-dir>...
"""
import re, sys, datetime
from pathlib import Path

TICK = r"(?:⬜|🔨|🧠|✅|❄️?|🟡|🟠|⏸️?)"
AROW = re.compile(rf"^- (?:{TICK}\s+)?(A(\d+)\.(\d+))\s+·\s+")
PROW = re.compile(rf"^- (?:{TICK}\s+)?P(\d+)\s+·\s+")

def section_span(lines, name):
    s = next((i for i, l in enumerate(lines) if l.strip() == f"## {name}"), None)
    if s is None: return None
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return s, e

def n_divisions(lines):
    sp = section_span(lines, "Content")
    if not sp: return 0
    n, fence = 0, False
    for l in lines[sp[0] + 1:sp[1]]:
        if l.lstrip().startswith("```"): fence = not fence
        if not fence and re.match(r"^### \S", l): n += 1
    return n

def blocks(body):
    """Aims body -> [(heading or None, [lines])] split on ### headings."""
    out, cur = [], (None, [])
    for l in body:
        if l.startswith("### "):
            out.append(cur); cur = (l, [])
        else:
            cur[1].append(l)
    out.append(cur)
    return out

def rows(lines):
    out, cur = [], None
    for l in lines:
        if l.startswith("- "):
            if cur: out.append(cur)
            cur = [l]
        elif cur is not None and (l.startswith("  ") or not l.strip()):
            cur.append(l)
        else:
            if cur: out.append(cur); cur = None
            out.append([l])
    if cur: out.append(cur)
    return out

def fold(page):
    text = page.read_text(encoding="utf-8"); lines = text.split("\n")
    sp = section_span(lines, "Aims")
    if not sp: return None
    nd = n_divisions(lines)
    head_lines = lines[sp[0] + 1:sp[1]]
    bl = blocks(head_lines)
    orphans = [(h, b) for h, b in bl if h and (m := re.match(r"^### A(\d+)\b", h)) and int(m.group(1)) > nd]
    if not orphans: return None
    all_text = "\n".join(head_lines)
    pmax = max([int(x) for x in re.findall(r"(?m)^- (?:%s\s+)?P(\d+)\s+·" % TICK, all_text)] or [0])
    # plan ids too, so a P the plan already uses is not reused
    plans = sorted((page.parent / "outline").glob(f"{page.stem}-outline-v*.md"))
    latest = plans[-1] if plans else None
    if latest:
        pmax = max(pmax, *([int(x) for x in re.findall(r"\bP(\d+)\b", latest.read_text(encoding="utf-8"))] or [0]))
    mapping, moved, folded_names = {}, [], []
    for h, b in orphans:
        folded_names.append(re.sub(r"^### ", "", h).strip())
        for r in rows(b):
            m = AROW.match(r[0])
            if not m:
                if r[0].strip(): moved.append(r)   # a stray line under the group travels too
                continue
            pmax += 1; new = f"P{pmax}"; mapping[m.group(1)] = new
            r = [r[0].replace(m.group(1), new, 1)] + r[1:]
            moved.append(r)
    # rebuild Aims: drop orphan groups, append moved rows to ### P (create at end)
    kept = [(h, b) for h, b in bl if (h, b) not in orphans]
    pidx = next((i for i, (h, b) in enumerate(kept) if h and re.match(r"^### P\b", h)), None)
    moved_lines = [l for r in moved for l in r]
    if pidx is None:
        kept.append(("### P · Page-level", [""] + moved_lines + [""]))
    else:
        h, b = kept[pidx]
        while b and not b[-1].strip(): b.pop()
        kept[pidx] = (h, b + moved_lines + [""])
    new_body = []
    for h, b in kept:
        if h is not None: new_body.append(h)
        new_body.extend(b)
    lines[sp[0] + 1:sp[1]] = new_body
    new_text = "\n".join(lines)
    # rename ids inside the page text (Content/Discussion references)
    for old, new in mapping.items():
        new_text = re.sub(rf"\b{re.escape(old)}\b", new, new_text)
    # safety: every moved row head text reappears
    lost = []
    for r in moved:
        key = re.sub(rf"^- (?:{TICK}\s+)?(?:A\d+\.\d+|P\d+)\s+·\s+", "", r[0]).strip()
        if key and key not in new_text: lost.append(key[:80])
    return dict(page=page, ndiv=nd, folded=folded_names, mapping=mapping, new_text=new_text, lost=lost, latest=latest)

def rename_in(path, mapping):
    t = path.read_text(encoding="utf-8"); n = 0
    for old, new in mapping.items():
        t, k = re.subn(rf"\b{re.escape(old)}\b", new, t); n += k
    if n: path.write_text(t, encoding="utf-8")
    return n

def main():
    args = sys.argv[1:]; write = "--write" in args
    boards = [Path(a) for a in args if not a.startswith("--")]
    total = 0
    for board in boards:
        pages = sorted(p for p in board.glob("*/*/*.md") if "_archive" not in p.parts and p.parent.name == p.stem)
        for page in pages:
            r = fold(page)
            if not r: continue
            total += len(r["mapping"])
            flag = "LOST " if r["lost"] else "ok   "
            print(f"{flag}{page.stem}: divs {r['ndiv']} · folded {r['folded']} · {r['mapping']}")
            for l in r["lost"]: print("      lost:", l)
            if not write or r["lost"]: continue
            page.write_text(r["new_text"], encoding="utf-8")
            touched = []
            for f in sorted((page.parent / "outline").glob("*.md")):
                if re.search(r"-outline-v\d+\.md$", f.name) and f != r["latest"]:
                    continue                      # frozen history
                if rename_in(f, r["mapping"]): touched.append(f.name)
            log = page.parent / "outline" / f"{page.stem}-log.md"
            if log.is_file():
                t = log.read_text(encoding="utf-8")
                stamp = datetime.datetime.now().strftime("%y%m%d %H%M")
                rec = (f"### {stamp} · Aim groups past the Content divisions folded into P: "
                       + "; ".join(f"{k} → {v}" for k, v in r["mapping"].items()) + "\n"
                       f"  Groups folded: {', '.join(r['folded'])}. Rule: `A<n>` is the n-th Content division; a group with no division is page-level (JL 260831). Ids renamed in the page, the latest plan and the live records.\n\n")
                m = re.search(r"(?m)^### ", t)
                t = (t[:m.start()] + rec + t[m.start():]) if m else (t.rstrip("\n") + "\n\n" + rec)
                log.write_text(t, encoding="utf-8")
            print(f"      written · renamed in: {touched}")
    print(f"{'written' if write else 'would move'} {total} rows")

if __name__ == "__main__":
    main()
