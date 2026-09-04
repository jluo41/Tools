#!/usr/bin/env python3
"""⓪ COLLECT · project every Round's rows routed to ONE page into its register.

    python3 cli/feedback.py collect <page.md>          one page
    python3 cli/feedback.py collect --all <board>      every non-round page
    python3 cli/feedback.py reopen <board>             which pages a Round REOPENS
                                                       at OUTLINE, in the order the
                                                       Round's own gates impose

PULL, not push: the page collects its own feedback during OUTLINE; a Round
stays read-only toward other pages. Rows are DERIVED and VERBATIM: the head,
the ids, the Round's own `Feedback:` and `Work:` sentences, and the full
concern of each parent R-row (0.17.4; head-only rows lost the substance, JL
260831). `landed:` is the page's pen and survives a re-run.
The register is outline/<stem>-feedback.md, one file grouped by Round (haipipe-plugin-outline 0.17.0).
"""
import argparse, re, sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from src.feedback import rounds, parse_round, register_path, read_landed  # noqa: E402


def collect(page_md: Path, board: Path) -> list[str]:
    pid = page_md.stem.split("-")[0]
    reg = register_path(page_md)
    landed = read_landed(reg)
    groups, total, n_open, n_land = [], 0, 0, 0
    for rd in rounds(board):
        data = parse_round(rd)
        rows = data["rows"].get(pid, [])
        if not rows:
            continue
        verdict = data["verdicts"].get(pid)
        head = rd.read_text(encoding="utf-8", errors="replace")[:1200]
        recv = re.search(r"(?m)^received-at:\s*(.+)$", head)
        frm = re.search(r"(?m)^received-from:\s*(.+)$", head)
        title = re.search(r"(?m)^# [A-Z]{2}\d{2} · (.+)$", head)
        rdid = rd.stem.split("-")[0]
        rel = Path(*([".."] * 3)) / rd.parent.name / rd.name
        # the Round's own block stays TEXT, not a `###` record, so the chip
        # count equals the routed rows (status says "8 of 8", the chip says 8)
        g = [f"## {rdid} · {title.group(1).strip() if title else rd.stem}",
             f"**{verdict[0] if verdict else 'routed by the ledger'}** · "
             f"{frm.group(1) if frm else '—'} · {recv.group(1) if recv else '—'} · "
             f"[{rel.name}]({rel}) §2A §2B", ""]
        if verdict:
            g += [f"**Ask** · {verdict[1]}", ""]
            if len(verdict) > 3 and verdict[3]:
                g += [f"**Order** · {verdict[3]}", ""]
            g += [f"**Gate** · {verdict[2]}", ""]
        for r in rows:
            # one RECORD per row, the folder's one shape (haipipe-plugin-outline 0.18.0);
            # Feedback / Work are the Round's words, copied whole (0.17.4); the
            # parent R-row's concern is folded detail under the card, not a row
            g += [f"### {r['id']} · {r['head']}",
                  f"- **From**: {r['parent'] or '—'} · {r['anchors'] or '—'}"]
            if r.get("feedback"):
                g += [f"- **Feedback**: {r['feedback']}"]
            if r.get("work"):
                g += [f"- **Work**: {r['work']}"]
            g += [f"- **State**: {r['state']}",
                  f"- **Landed**: {landed.get(r['id'], '—')}"]
            for q, concern, qpages in r.get("parents", []):
                g += [f"  ↳ {q} · {concern} → routes {', '.join(sorted(qpages))}"]
            g += [""]
            total += 1
            n_open += r["state"] == "open"
            n_land += landed.get(r["id"], "—") not in ("", "—")
        groups.append("\n".join(g))
    if not groups:
        return []
    # three header lines and one sentence; the law lives in the skill, not here
    out = [f"# {page_md.stem} · feedback", f"page: {page_md.stem}",
           f"kind: feedback · generated {date.today():%y%m%d} by cli/feedback.py collect · only Landed is this page's",
           f"status: {n_open} of {total} open · {n_land} landed · {len(groups)} round(s)", "",
           "The Round's own words, copied. To argue with a row, open a `D<nn>` thread in `-discussion.md` naming it.", ""]
    reg.parent.mkdir(parents=True, exist_ok=True)
    reg.write_text("\n".join(out) + "\n\n" + "\n\n".join(groups) + "\n", encoding="utf-8")
    return [f"{reg.relative_to(board)}  {len(groups)} round(s) · {total} rows · {n_open} open · {n_land} landed"]


def reopen(board: Path) -> list[str]:
    """A Round never dispatches agents; it DECLARES reopenings. This lists them.

    Every page with >=1 open routed row is reopened at OUTLINE. The order is
    the Round's own: a page whose §2A gate names another page waits for it
    (SM01 waits on NA01, SM08 on SM03/SM06/SM07). Running the fold is the
    existing per-page RUN (haipipe-page-workflow -> outline agent), one page
    at a time or under a signed charter; never a blind 15-way fan-out."""
    from src.feedback import PAGE_ID
    out, waits, opens, sig = [], {}, {}, {}
    for rd in rounds(board):
        data = parse_round(rd)
        ledger = data.get("ledger", {})
        for pid, rows in data["rows"].items():
            n = sum(1 for r in rows if r["state"] == "open")
            if not n:
                continue
            opens[pid] = opens.get(pid, 0) + n
            sig[pid] = tuple(sorted(r["id"] for r in rows))
            gate = data["verdicts"].get(pid, ("", "", ""))[2]
            deps = {d for d in PAGE_ID.findall(gate) if d != pid}
            # the Round's routing table: a concern that also routes to a
            # Narrative is ruled there first, so this page waits on it
            for r in rows:
                for par in re.findall(r"R\d{2}", r["parent"]):
                    deps |= {q for q in ledger.get(par, {}).get("pages", set())
                             if q.startswith("NA") and q != pid}
            waits[pid] = waits.get(pid, set()) | deps
    # pages sharing one §2B block (SM04 + SM05 under a proposed merge) are ONE
    # reopening; collapse them and drop their mutual waits
    groups = {}
    for pid, sg in sig.items():
        groups.setdefault(sg, []).append(pid)
    unit = {pid: " + ".join(sorted(g)) for g in groups.values() for pid in g}
    uw, uo = {}, {}
    for pid in opens:
        u = unit[pid]
        uo[u] = opens[pid]
        uw[u] = uw.get(u, set()) | {unit.get(d, d) for d in waits[pid]} - {u}
    done, order, pending = set(), [], dict(uw)
    while pending:
        ready = sorted(p for p, d in pending.items() if not (d - done))
        if not ready:
            ready = [sorted(pending)[0]]
        for p in ready:
            order.append(p); done.add(p); pending.pop(p)
    waits, opens = uw, uo
    for i, pid in enumerate(order, 1):
        w = ", ".join(sorted(waits[pid])) or "—"
        out.append(f"{i:>2}  {pid:<6} {opens[pid]:>3} open   waits on: {w}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("verb", choices=["collect", "reopen"])
    ap.add_argument("target", type=Path)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.verb == "reopen":
        for line in reopen(a.target):
            print(line)
        return
    if a.all:
        board = a.target
        pages = [md for md in sorted(board.glob("*/*/*.md"))
                 if md.parent.name == md.stem and "_archive" not in md.parts
                 and not re.search(r"(?m)^page-type:\s*round\b", md.read_text(errors="replace")[:600])]
    else:
        board = a.target.parents[2]
        pages = [a.target]
    for p in pages:
        for line in collect(p, board):
            print(line)


if __name__ == "__main__":
    main()
