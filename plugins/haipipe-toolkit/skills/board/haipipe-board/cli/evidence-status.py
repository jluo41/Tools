#!/usr/bin/env python3
"""Write `outline/<stem>-evidence.md`: the ITEM TABLE joined to the disk.

    python3 evidence-status.py <page.md>            one page
    python3 evidence-status.py --all <board-dir>    every page that has a plan

One record per marked plan bullet, in the folder's one record shape
(`### <address> · <mark> <the plan's words>` + label rows). The AUTHORED half
of each record is copied from `outline/<stem>-items.md` (Need · Route · Run ·
Decide, written at SURVEY, `haipipe-plugin-outline/ref/item-table.md`); the
DERIVED half is computed here (Has · Status). Status is one word of the item
ladder, never typed by anyone:

    owed → bound → landed → folded → accepted   (+ stale · deferred · dropped · blocked)

WHY A FILE beside the live 🧭 tab (JL 260831): a person can read it with no
server, `git diff` shows what landed since yesterday, and a CHECK receipt can
quote "4 items · 2 landed". WHY IT IS GENERATED ONLY: a hand-typed `landed`
outranks the disk the moment it is typed. Nobody writes into this file; the
ticks stay on their owners (`Decide` on the item row, `verified` on the key,
`accepted:` on the page) and this file only reports them. `check.py` reports
`evidence-stale` when any lane, the plan or the item table is newer than the
stamp.

The plan parse is `live/outline.py`'s, imported, so the file and the 🧭 tab
cannot disagree: same plan parse, same disk state, same per-mark verdict.
"""
import argparse, datetime, importlib.util, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))  # live/outline.py imports src.common
_spec = importlib.util.spec_from_file_location("live_outline", HERE / "live" / "outline.py")
lo = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(lo)

BEGIN, END = "# --- evidence-status:begin (generated) ---", "# --- evidence-status:end ---"
from src.item_table import (LADDER, EMOJI, OUTCOMES, CYCLES, MARKS, repo_root,  # noqa: E402
                            read_items, resolve as _exists, bullets, item_status, cycle_now)


def build(page_md: Path) -> str:
    plan, ver = lo._latest_plan(page_md)
    if plan is None:
        return ""
    cards, units, keys, serves, display_serves = lo._disk_state(page_md)
    page_txt = page_md.read_text(encoding="utf-8", errors="replace")
    # Aims live on the PAGE again (JL 260831, QPf12-outline row 2); the plan
    # is the fallback for a page not yet reverted.
    aims = lo._aim_rows(page_txt) or \
           lo._aim_rows(plan.read_text(encoding="utf-8", errors="replace"))
    plan_txt = plan.read_text(errors="replace")
    approved = bool(re.search(r"^approved:\s*✅", plan_txt, re.M))
    page_accepted = bool(re.search(r"^accepted:\s*✅", page_txt, re.M))
    items = read_items(page_md)
    root, page_dir = repo_root(page_md.parent), page_md.parent
    plan_mtime = plan.stat().st_mtime
    rows, counts, statuses = [], {w: 0 for w in LADDER}, []
    # The ↩ backlink: a card or unit names the bullets it SERVES, so a BARE
    # mark whose bullet already has a card is RAISED (the plan is frozen
    # before the card exists). Reading marks alone printed 37 "not raised"
    # rows on SM06 for bullets its cards already served.
    by_bullet = {}
    for pid, addrs in serves.items():
        for a in addrs: by_bullet.setdefault(a, []).append(pid)
    for did, addrs in display_serves.items():
        for a in addrs: by_bullet.setdefault(a, []).append(did)
    n_marks = 0
    for addr, head, kind, refs, folded in bullets(plan_txt):
        if kind is None or kind == "aim":
            continue
        n_marks += 1
        if not refs and by_bullet.get(addr):
            want = "Display" if kind == "display" else "PP"
            refs = [x for x in by_bullet[addr] if x.startswith(want)] or [""]
        ref = (refs or [""])[0]
        cls, note, _detail = lo._live(kind, ref, cards, units, keys, aims)
        row = items.get(addr)
        lane_ok = cls == "ok"
        st = item_status(row, lane_ok, lane_ok and ("accepted" in note or "verified" in note),
                         folded, page_accepted, plan_mtime, root, page_dir)
        counts[st] += 1; statuses.append(st)
        emo = {v: k for k, v in MARKS.items()}[kind]
        # One record per bullet, the folder's one shape: the head CARRIES THE
        # WORDS (JL 260831 "it lost a lot of informations"). The authored
        # half is copied from the item table verbatim; a bullet with no row
        # says so, which is the SURVEY still owed.
        lines = [f"### {addr} · {emo} {head or '—'}", f"- **Status**: {EMOJI[st]} {st}"]
        if row:
            lines += [f"- **Need**: {row['need'] or '—'}",
                      f"- **Route**: {row['route'] or '—'}",
                      f"- **Run**: {row['run'] or '—'}",
                      f"- **Decide**: {row['decide'] or '☐'}"]
        else:
            lines.append("- **Run**: not surveyed yet")
        lines.append(f"- **Has**: {note.strip()}" + (f" · {ref}" if ref else ""))
        rows.append("\n".join(lines))
    cyc = cycle_now(approved, items, statuses, n_marks)
    now = datetime.datetime.now().strftime("%y%m%d %H%M")
    tally = " · ".join(f"{w} {counts[w]}" for w in LADDER if counts[w]) or "nothing owed"
    decided = sum(1 for r in items.values() if r["decision"])
    head = [f"# {page_md.stem} · evidence status", f"page: {page_md.stem}",
            "kind: evidence · ⚙️ derived · never hand-edited · the item table joined to the disk", "",
            BEGIN, f"  EVIDENCE STATUS, MEASURED {now}. GENERATED; do not hand-edit.",
            f"  regenerate: cli/evidence-status.py {page_md.name}", "",
            f"plan: {ver} · approved: {'✅' if approved else '⬜'} · cycle: {cyc} · items {n_marks}"
            f" · decided {decided}/{len(items) or n_marks} · {tally}", ""]
    return "\n".join(head + ["\n\n".join(rows) if rows else "(no marked bullet in the plan)"] + ["", END, ""])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("target", type=Path); ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    pages = ([p / f"{p.name}.md" for g in a.target.iterdir() if g.is_dir() and not g.name.startswith(("_", ".", "board"))
              for p in g.iterdir() if p.is_dir() and (p / f"{p.name}.md").exists()] if a.all else [a.target])
    n = 0
    for pg in pages:
        txt = build(pg)
        if not txt: continue
        out = pg.parent / "outline" / f"{pg.stem}-evidence.md"
        out.write_text(txt, encoding="utf-8"); n += 1
        print(f"wrote {out.relative_to(Path.cwd()) if out.is_relative_to(Path.cwd()) else out}")
    print(f"{n} file(s)")
if __name__ == "__main__":
    sys.exit(main())
