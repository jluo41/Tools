#!/usr/bin/env python3
"""Write `outline/<stem>-evidence.md`: one bullet, one RECORD, what it owes and
what has landed, in the Evidence Bundle's own six status words
(`### <address> · <mark> <the plan's words>` + Has / Ref / Status rows, 0.18.1).

    python3 evidence-status.py <page.md>            one page
    python3 evidence-status.py --all <board-dir>    every page that has a plan

WHY A FILE beside the live 🧭 tab (JL 260831): a person can read it with no
server, `git diff` shows what landed since yesterday, and a CHECK receipt can
quote "12 owed, 9 landed". WHY IT IS GENERATED ONLY: a hand-typed `✅ landed`
outranks the disk the moment it is typed. Nobody writes into this file; the
ticks stay on their owners (`read:` on the card, `verified` on the key,
`accepted:` on the unit) and this file only reports them. `check.py` reports
`evidence-stale` when any card, key, unit or the plan is newer than the stamp.

The join is `live/outline.py`'s, imported, so the file and the 🧭 tab cannot
disagree: same plan parse, same disk state, same per-mark verdict.
"""
import argparse, datetime, importlib.util, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("live_outline", HERE / "live" / "outline.py")
lo = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(lo)

BEGIN, END = "# --- evidence-status:begin (generated) ---", "# --- evidence-status:end ---"
# A probe id is `PP<NN>` standing alone: `S0-PP2` in a `Routed:` line is a Round row id,
# not a card (found 260831: SM00 printed "📮 PP2 · no card" for a bare mark).
REFPAT = {"probe": r"(?<![A-Za-z0-9-])(PP\d+)", "value": r"(?<![A-Za-z0-9-])(PP\d+(?:\.v\d+)?)", "display": r"(Display\d+)",
          "cite": r"(QB\d+|[A-Za-z][\w:-]*\d{4}[A-Za-z]*|[A-Za-z][\w-]*[_:][\w:-]+|[A-Z][A-Z0-9-]{3,})", "aim": r"(?<![A-Za-z0-9.\-])(A\d+\.\d+|P\d+)"}
# ref/evidence-bundle.md §Status rule: six words, no seventh.
def status(kind, cls, note):
    if kind == "aim":
        return "aim"
    if cls == "ok":
        return "accepted" if ("accepted" in note or "verified" in note) else "evidence-ready"
    if kind == "probe":
        return "needs-probe" if "not raised" in note or "no card" in note else "needs-revision"
    if kind == "value":
        return "needs-probe" if "no card" in note else "needs-revision"
    if kind == "display":
        return "needs-intake" if ("not built" in note or "not rendered" in note or "no unit" in note or "intake" in note) else "needs-revision"
    if kind == "cite":
        return "needs-citation"
    return "needs-revision"

def bullets(plan_text):
    """Walk the plan: (address, head, kind, refs) for every marked bullet.

    A bullet is its `- B<n> ·` or `- S<n> ·` head line PLUS its folded continuation lines
    (`  Note: … 🎯 A1.1`), exactly as `plan_card` assembles it: the end mark
    normally sits on the Note line, so a walker that reads heads alone finds
    no marks at all (found on SM08's first run: "no marked bullet").
    """
    lines = plan_text.splitlines()
    c = p = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^## C(\d+)\b", line)
        if m: c, p = int(m.group(1)), 0; i += 1; continue
        m = re.match(r"^### C(\d+)\.P(\d+)\b", line)
        if m: c, p = int(m.group(1)), int(m.group(2)); i += 1; continue
        if re.match(r"^## Aims\b", line): break
        m = re.match(r"^- (?:\[[ xX]\] )?[BS](\d+)\s*·\s*(.*)$", line)
        # [BS]: a Section plan's sentence slots are `- S<n> ·` (the 0.5.x
        # slot grammar); slot number == position, so S<n> and B<n> are ONE
        # address and the wall keys them canonically as B (JAMA repro 260831:
        # SA01-SA04 reported "no marked bullet" with marks bound).
        if not m: i += 1; continue
        b, head = int(m.group(1)), m.group(2).strip()
        body, j = m.group(2), i + 1
        while j < len(lines) and lines[j].startswith("  ") and not lines[j].lstrip().startswith("- "):
            body += " " + lines[j].strip(); j += 1
        i = j
        hit, hit_at = None, -1
        aim_hit, aim_at = None, -1
        for emo, kind in lo._MARK.items():
            at = body.rfind(emo)
            if at < 0:
                continue
            # 🎯 ANNOTATES a bullet; it never changes its evidence kind.
            # A "📮 PP02   🎯 A5.1" bullet is a probe row (JAMA repro 260831:
            # SA04 read owed 0 with both slots marked; SM03's 🖼+🎯 dropped).
            if kind == "aim":
                if at > aim_at: aim_hit, aim_at = (emo, kind), at
                continue
            if at > hit_at: hit, hit_at = (emo, kind), at
        if hit is None and aim_hit is not None:
            hit, hit_at = aim_hit, aim_at
        if hit is None:
            yield f"C{c}.P{p}.B{b}", head, None, []
            continue
        emo, kind = hit
        refs = re.findall(REFPAT[kind], body[hit_at + len(emo):]) if kind in REFPAT else []
        yield f"C{c}.P{p}.B{b}", head, kind, refs

def build(page_md: Path) -> str:
    plan, ver = lo._latest_plan(page_md)
    if plan is None:
        return ""
    cards, units, keys, serves, display_serves = lo._disk_state(page_md)
    # Aims live on the PAGE again (JL 260831, QPf12-outline row 2); the plan
    # is the fallback for a page not yet reverted.
    aims = lo._aim_rows(page_md.read_text(encoding="utf-8", errors="replace")) or \
           lo._aim_rows(plan.read_text(encoding="utf-8", errors="replace"))
    approved = bool(re.search(r"^approved:\s*✅", plan.read_text(errors="replace"), re.M))
    rows, owed = [], {"owed": 0, "landed": 0, "accepted": 0}
    # The ↩ backlink: a card or unit names the bullets it SERVES, so a BARE
    # mark whose bullet already has a card is RAISED (the plan is frozen
    # before the card exists). Reading marks alone printed 37 "not raised"
    # rows on SM06 for bullets its cards already served.
    by_bullet = {}
    for pid, addrs in serves.items():
        for a in addrs: by_bullet.setdefault(a, []).append(pid)
    for did, addrs in display_serves.items():
        for a in addrs: by_bullet.setdefault(a, []).append(did)
    for addr, head, kind, refs in bullets(plan.read_text(encoding="utf-8", errors="replace")):
        if kind is None or kind == "aim":
            continue
        owed["owed"] += 1
        if not refs and by_bullet.get(addr):
            want = "Display" if kind == "display" else "PP"
            refs = [x for x in by_bullet[addr] if x.startswith(want)] or [""]
        for ref in (refs or [""]):
            cls, note, _detail = lo._live(kind, ref, cards, units, keys, aims)
            st = status(kind, cls, note)
            if st in ("evidence-ready", "accepted"): owed["landed"] += 1
            if st == "accepted": owed["accepted"] += 1
            emo = {v: k for k, v in lo._MARK.items()}[kind]
            # One record per bullet, the folder's one shape (0.18.1):
            # `### <address> · <mark> <the plan's own words>` then Has / Ref /
            # Status rows. The head CARRIES THE WORDS (JL 260831 "it lost a
            # lot of informations" + tonight "kind of hard and ugly"): an
            # address with a bare ref told a reader nothing about WHAT is
            # owed; the ref moved to its own row and shows only when real.
            rows.append(f"### {addr} · {emo} {head or '—'}\n- **Has**: {note.strip()}"
                        + (f"\n- **Ref**: {ref}" if ref else "")
                        + f"\n- **Status**: {st}")
    worst = ("needs-probe" if any(r.endswith("needs-probe") for r in rows) else
             "needs-intake" if any(r.endswith("needs-intake") for r in rows) else
             "needs-citation" if any(r.endswith("needs-citation") for r in rows) else
             "needs-revision" if any(r.endswith("needs-revision") for r in rows) else
             "accepted" if rows and owed["accepted"] == len(rows) else "evidence-ready")
    now = datetime.datetime.now().strftime("%y%m%d %H%M")
    head = [f"# {page_md.stem} · evidence status", f"page: {page_md.stem}", "kind: evidence · ⚙️ derived · never hand-edited", "",
            BEGIN, f"  EVIDENCE STATUS, MEASURED {now}. GENERATED; do not hand-edit.",
            f"  regenerate: cli/evidence-status.py {page_md.name}", "",
            f"plan: {ver} · approved: {'✅' if approved else '⬜'}      owed {owed['owed']} · landed {owed['landed']} · accepted {owed['accepted']} · status: {worst}", ""]
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
