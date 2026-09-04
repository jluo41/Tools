#!/usr/bin/env python3
"""Merge a page's retired `## States` into `## Aims` (haipipe-page 0.41.0 / haipipe-board 0.148.0).

Rules, all derived from the contract:
  tick row   `- 🧠 A1.1 · fact`            -> tick onto the Aim row, `**Now:** fact` under its Done when
  Needs JL   `- ✋ ask` naming an Aim id    -> that Aim's `**Now:** 🧠 ask`
             `- ✋ ask` naming none         -> stays verbatim, group moved under ## Aims
  Decision   `### Decision Now` group       -> moved verbatim to the TOP of ## Aims
  anything else (#### blocks, prose, bare rows) -> verbatim under ## Discussion (created if absent)
Safety net: every non-blank, non-heading line of the old States, stripped of its list marker /
tick / checkbox, must reappear verbatim in the new page, or the page is not written.
Usage: states_merge.py [--write] [--backup DIR] <page.md>...
"""
import re, sys, shutil, datetime
from pathlib import Path

AIM_ID = r"(?:A\d+(?:\.\d+)*|P\d+(?:\.\d+)*)"
TICK = r"(?:⬜|🔨|🧠|✅|❄️?|🟡|🟠|⏸️?)"
TICK_ROW = re.compile(rf"^- ({TICK})\s+({AIM_ID})\s+·\s+(.*)$")
AIM_ROW = re.compile(rf"^- (?:{TICK}\s+)?({AIM_ID})\s+·\s+(.*)$")
ASK_ROW = re.compile(r"^- (✋|\[ \]|\[x\])\s*(.*)$")
NEEDS_H = re.compile(r"^### Needs JL", re.I)
DECISION_H = re.compile(r"^### Decision Now", re.I)

def sections(lines):
    """[(heading or None, [lines])] split on `## ` headings, fences respected."""
    out, cur, fence = [], (None, []), False
    for ln in lines:
        if ln.lstrip().startswith("```"): fence = not fence
        if ln.startswith("## ") and not fence:
            out.append(cur); cur = (ln, [])
        else:
            cur[1].append(ln)
    out.append(cur)
    return out

def norm(ln):
    s = ln.strip()
    s = re.sub(rf"^[-*]\s+(?:{TICK}|✋|\[ \]|\[x\]|🗣)?\s*", "", s)
    s = re.sub(r"^\*\*Now:\*\*\s*", "", s)
    s = re.sub(rf"^(?:{TICK})\s*", "", s)
    s = re.sub(rf"^{AIM_ID}\s+·\s+", "", s)
    return s

def groups(body):
    """Split a States body into (heading-or-None, lines) on ### / #### headings."""
    out, cur = [], (None, [])
    for ln in body:
        if ln.startswith("### ") or ln.startswith("#### "):
            out.append(cur); cur = (ln, [])
        else:
            cur[1].append(ln)
    out.append(cur)
    return [(h, b) for h, b in out if h is not None or any(x.strip() for x in b)]

def rows(lines):
    """Group list rows with their indented continuation lines."""
    out, cur = [], None
    for ln in lines:
        if ln.startswith("- "):
            if cur: out.append(cur)
            cur = [ln]
        elif cur is not None and (ln.startswith("  ") or not ln.strip()):
            cur.append(ln)
        else:
            if cur: out.append(cur); cur = None
            out.append([ln])
    if cur: out.append(cur)
    return out

def migrate(text):
    lines = text.split("\n")
    secs = sections(lines)
    names = [h.strip() if h else None for h, _ in secs]
    if "## States" not in names or "## Aims" not in names:
        return None, "no States or no Aims"
    si = names.index("## States"); ai = names.index("## Aims")
    states_body = secs[si][1]
    old_lines = [norm(l) for l in states_body if l.strip() and not l.startswith("#")]
    ticks, nows, decision, kept_asks, discussion = {}, {}, [], [], []
    page_aims = set(m.group(1) for l in secs[ai][1] for m in [AIM_ROW.match(l)] if m)
    for h, body in groups(states_body):
        if h and DECISION_H.match(h):
            decision.append(h); decision.extend(body); continue
        if h and h.startswith("#### "):
            discussion.append(h); discussion.extend(body); continue
        is_needs = bool(h and NEEDS_H.match(h))
        pending = [h] if (h and not is_needs and not re.match(rf"^### {AIM_ID}\b|^### A\d", h)) else []
        for r in rows(body):
            head = r[0]
            m = TICK_ROW.match(head)
            if m and m.group(2) not in page_aims:
                discussion.extend(r); continue
            if m:
                emoji, aid, fact = m.group(1), m.group(2), m.group(3).strip()
                ticks[aid] = emoji
                nows.setdefault(aid, []).append((fact, r[1:]))
                continue
            a = ASK_ROW.match(head)
            if a and is_needs:
                ids = [x for x in re.findall(rf"\b({AIM_ID})\b", head) if x in page_aims]
                if ids:
                    aid = ids[0]
                    ticks.setdefault(aid, "🧠")
                    nows.setdefault(aid, []).append(("🧠 " + a.group(2).strip(), r[1:]))
                else:
                    kept_asks.append(r)
                continue
            if not head.strip():
                continue
            # anything else lands in Discussion verbatim
            if pending: discussion.extend(pending); pending = []
            discussion.extend(r)
        if is_needs and kept_asks and (not discussion or True):
            pass
    # ---- rewrite Aims
    aims_h, aims_body = secs[ai]
    new_aims, seen_aims = [], set()
    i = 0
    while i < len(aims_body):
        ln = aims_body[i]
        m = AIM_ROW.match(ln)
        if not m:
            new_aims.append(ln); i += 1; continue
        aid, rest = m.group(1), m.group(2)
        block = [ln]; j = i + 1
        while j < len(aims_body) and (aims_body[j].startswith("  ") or (not aims_body[j].strip() and j + 1 < len(aims_body) and aims_body[j + 1].startswith("  "))):
            block.append(aims_body[j]); j += 1
        if aid in ticks and not re.match(rf"^- {TICK}\s", ln):
            block[0] = f"- {ticks[aid]} {aid} · {rest}"
        if aid in nows:
            now_lines = []
            for fact, cont in nows[aid]:
                now_lines.append(f"  **Now:** {fact}")
                now_lines.extend(cont)
            # after the Done when line if present, else at block end
            k = next((x for x in range(len(block)) if "**Done when:**" in block[x]), None)
            if k is not None:
                # include the Done when's own continuation lines
                k += 1
                while k < len(block) and block[k].startswith("  ") and not re.match(r"^  \*\*\w", block[k]): k += 1
                block = block[:k] + now_lines + block[k:]
            else:
                while block and not block[-1].strip(): block.pop()
                block += now_lines
            seen_aims.add(aid)
        new_aims.extend(block); i = j
    unmatched = sorted(set(nows) - seen_aims)
    if unmatched:
        # an Aim named in States but absent from Aims: keep its rows verbatim in Discussion
        for aid in unmatched:
            for fact, cont in nows[aid]:
                discussion.append(f"- {ticks.get(aid, '⬜')} {aid} · {fact}"); discussion.extend(cont)
    # Decision Now + kept asks go FIRST inside Aims (after the heading's intro lines up to the first ###/row)
    lead = []
    if decision:
        lead += decision + [""]
    if kept_asks:
        lead += ["### Needs JL · tick these"]
        for r in kept_asks: lead += r
        lead += [""]
    if lead:
        # insert before the first ### or list row of Aims
        k = next((x for x in range(len(new_aims)) if new_aims[x].startswith("### ") or new_aims[x].startswith("- ")), len(new_aims))
        new_aims = new_aims[:k] + lead + new_aims[k:]
    secs[ai] = (aims_h, new_aims)
    # ---- Discussion
    if discussion:
        while discussion and not discussion[-1].strip(): discussion.pop()
        di = names.index("## Discussion") if "## Discussion" in names else None
        add = ["", "### From the retired States section (merged 260831)"] + discussion + [""]
        if di is not None:
            secs[di] = (secs[di][0], secs[di][1] + add)
        else:
            secs.insert(si, ("## Discussion", add))
            names.insert(si, "## Discussion"); si += 1
    # ---- drop States, add a Log row
    del secs[si]; del names[si]
    if "## Log" in names:
        li = names.index("## Log")
        stamp = datetime.datetime.now().strftime("%y%m%d %H%M")
        secs[li] = (secs[li][0], secs[li][1] + [f"- {stamp} · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0"])
    out = []
    for h, b in secs:
        if h is not None: out.append(h)
        out.extend(b)
    new_text = "\n".join(out)
    # ---- safety net
    new_norm = {norm(l) for l in out}
    lost = [l for l in old_lines if l and l not in new_norm]
    stats = dict(ticks=len([1 for a in nows]), asks_to_now=sum(1 for a in nows for f, _ in nows[a] if f.startswith("🧠 ")),
                 asks_kept=len(kept_asks), decision=1 if decision else 0, discussion=len(discussion), unmatched=unmatched, lost=lost)
    return new_text, stats

def main():
    args = sys.argv[1:]; write = "--write" in args
    backup = None
    if "--backup" in args:
        backup = Path(args[args.index("--backup") + 1]); backup.mkdir(parents=True, exist_ok=True)
    paths = [Path(a) for a in args if a.endswith(".md")]
    ok = 0
    for p in paths:
        text = p.read_text(encoding="utf-8")
        new, stats = migrate(text)
        if new is None:
            print(f"SKIP  {p.name}: {stats}"); continue
        flag = "LOST " if stats["lost"] else "ok   "
        print(f"{flag}{p.name}: ticks {stats['ticks']} · asks→Now {stats['asks_to_now']} · asks kept {stats['asks_kept']} · decision {stats['decision']} · discussion lines {stats['discussion']} · unmatched {stats['unmatched']}")
        for l in stats["lost"][:5]: print("      lost:", l[:110])
        if write and not stats["lost"]:
            if backup: shutil.copy2(p, backup / p.name)
            p.write_text(new, encoding="utf-8"); ok += 1
    if write: print(f"written {ok}/{len(paths)}")

if __name__ == "__main__":
    main()
