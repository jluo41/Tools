#!/usr/bin/env python3
"""The phase strip: where ONE Page sits in the five-phase Page workflow.

Three strips, three questions, and none substitutes for another:

    status.py       where is this SESSION      (board closing block, 3-4 rows)
    pagestatus.py   where is every page in a GROUP  (artifact counts)
    pagephase.py    which PHASE is this PAGE in     (this file)

The computation lives in `src/page_phase.py` and is shared with `status.py`'s
fourth row; this file only prints it. Never writes.

    python3 pagephase.py PAGE_DIR           the strip
    python3 pagephase.py PAGE_DIR --md      fenced, for pasting on a page
    python3 pagephase.py PAGE_DIR --row     the one-row form status.py prints
    python3 pagephase.py PAGE_DIR --owed    the LEDGER: every human tick still
                                            owed, one row each, with the
                                            approver's `checked:` beside it

The strip has always printed the owed COUNT. A count says there is a debt; it
never says where to spend the one act that is a person's. `--owed` is the LIST,
and it is the surface `QPw00g-human-gate` records as missing ("no surface joins
the owed ticks"). It is what makes one artifact serve both modes: in copilot you
watch it shrink, in auto you are handed it at the end. Its length is variable:
the owning phase may declare no Page RULING, reuse a domain gate, or require a
local one.

⚠️ The `→ now` row is the first phase whose exit test FAILS, read in loop
order. That is a REPORT, not a routing: which phase actually runs next is
decided by authority (haipipe-page's authority test), and CHECK may route
anywhere.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.page_phase import (  # noqa: E402
    EMOJI, LABEL, MARK, compact, phase_state, render_ledger)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", type=Path)
    ap.add_argument("--md", action="store_true", help="emit a fenced block")
    ap.add_argument("--row", action="store_true", help="the one-row form only")
    ap.add_argument("--owed", action="store_true",
                    help="the ledger: every human tick still owed, one row each")
    a = ap.parse_args()

    pd = a.page.resolve()
    md = pd / f"{pd.name}.md"
    st = phase_state(md)
    if st is None:
        print(f"not a page (no {pd.name}.md): {pd}", file=sys.stderr)
        return 2

    if a.row:
        print(compact(st))
        return 0

    if a.owed:
        if a.md:
            print("```text")
        print("\n".join(render_ledger(st)))
        if a.md:
            print("```")
        return 0

    m, o, tk = st["states"], st["outline"], st["ticks_owed"]
    mk = o["marks"]
    rec = st["receipt"]
    last = st["last"]
    disp, cards = st["displays"], st["cards"]

    L = [f"{st['page']} · phase strip (from disk, "
         f"{'receipt ' + rec['file'] if rec else 'no receipt'})"]
    row = lambda k: f"{MARK[m[k]]} {EMOJI[k]} {LABEL[k]:<14s}"
    ctx = st["context"]
    L.append(f"{row('CONTEXT')} "
             + (f"ready · {ctx['file'].name}" if ctx["file"] else "no context record"))
    it = st.get("items")
    L.append(f"{row('OUTLINE')} v{o['version']} "
             f"{'approved' if o['approved'] else ('UNAPPROVED' if o['file'] else 'no file')}"
             + (" · item types " + " ".join(
                 f"{kind} {count}" for kind, count in it["types"].items() if count
             ) if it and it["marks"] else
                f" · legacy marks 📮{mk['📮']} 🧮{mk['🧮']} 📚{mk['📚']} 🖼{mk['🖼']}")
             + (f" · items {it['rows']}/{it['marks']} · decided {it['decided']}/{it['rows']}"
                if it and it["rows"] else " · no item table yet"))
    if it and it["rows"]:
        c = it["counts"]
        L.append(f"{row('EVIDENCE')} " + " · ".join(f"{w} {c[w]}" for w in
                 ("specified", "planned", "ready", "folded", "accepted", "stale", "deferred", "dropped", "blocked") if c[w])
                 + f" · 📚 {st['bibex']['verified']}/{st['bibex']['entries']} verified"
                 + f" · 🖼 {len(st['drawn'])}/{len(disp)} drawn")
    else:
        L.append(f"{row('EVIDENCE')} 🧮 {len(st['answered'])}/{len(cards)} answered"
                 + (f" ({len(st['blocked'])} blocked)" if st["blocked"] else "")
                 + (f" · MISSING {','.join(st['missing'])}" if st["missing"] else "")
                 + f" · 📚 {st['bibex']['verified']}/{st['bibex']['entries']} verified"
                 + f" · 🖼 {len(st['drawn'])}/{len(disp)} drawn · {len(st['accepted'])}/{len(disp)} accepted")
    L.append(f"{row('CONTENT')} {st['divisions']} content divisions"
             + ("" if not o["file"] else
                (" · page edited AFTER outline tick" if st["page_after_tick"]
                 else " · page predates outline tick")))
    L[-1] += (f" · latex/ {'present' if st['latex'] else 'absent'}"
             + (f" · pdf {'fresh' if st['pdf_fresh'] else 'STALE/none'}" if st["latex"] else ""))
    L.append(f"{row('CHECK')} last receipt: "
             + (f"{last.get('phase')} → {last.get('route')} (round {last.get('round')})"
                if last else "none"))
    L.append(f"→ now: {st['now']} · cycle {st.get('cycle')} · ✋ human ticks still owed: {sum(tk.values())}"
             f" (read:{tk['read']} verified:{tk['verified']} accepted:{tk['accepted']}"
             f"{'' if not tk['approved'] else ' approved:1'}"
             f"{'' if not tk['ruling'] else ' ruling:1'})"
             + ("  — see them: --owed" if sum(tk.values()) else ""))
    L.append(compact(st))

    if a.md:
        print("```text")
    print("\n".join(L))
    if a.md:
        print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
