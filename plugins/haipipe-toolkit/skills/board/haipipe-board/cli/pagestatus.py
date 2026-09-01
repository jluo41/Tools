#!/usr/bin/env python3
"""One row per Page, one column per thing a Page can owe.

The three-line closing block (`status.py`) answers "where is this SESSION".
This answers a different question: "where is every page in this GROUP", and it
answers it from DISK rather than from what a page says about itself.

    python3 pagestatus.py BOARD                 every group
    python3 pagestatus.py BOARD --group QPw     one group
    python3 pagestatus.py BOARD --group QPw --md   markdown, for pasting on a page

Never writes. Every column is a count a person can go and verify.
"""
import argparse, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.common import evidence_lane_dirs  # noqa: E402

def _pages(board: Path, group: str | None):
    out = []
    for d in sorted(board.iterdir()):
        if not d.is_dir() or d.name.startswith(("_", ".")) or d.name in ("board", "fig", "draw"):
            continue
        for pd in sorted(d.iterdir()):
            if not pd.is_dir():
                continue
            md = pd / f"{pd.name}.md"
            if not md.exists():
                continue
            pid = re.match(r"([A-Za-z]+\d*[a-z]?)", pd.name)
            pid = pid.group(1) if pid else pd.name
            if group and not re.match(rf"^{group}\d*[a-z]?$", pid):
                continue
            out.append((pid, pd, md))
    return out

def _count(pd: Path, md: Path):
    t = md.read_text(encoding="utf-8", errors="replace")
    r = {}
    # Match check.py:1176's division grammar, not a narrower one. A Section
    # Page numbers its divisions by the MANUSCRIPT (`### §6.1 Main Results`),
    # which check.py accepts via `§?[\d.]+` and this file used to miss, so all
    # 15 Section Pages of a paper board read as `§ 0` (JL 260830: "it barely
    # doesn't work"). One grammar, one place.
    r["div"] = len(re.findall(r"^### §?[\d.]+(?: · | )\S", t, re.M))
    r["sub"] = len(re.findall(r"^#### §?[\d.]+(?: · | )\S", t, re.M))
    r["aim"] = len(re.findall(r"^- (?:[⬜🔨🧠✅❄️] )?[AP]\d+\.\d+ · ", t, re.M))
    r["st"]  = len(re.findall(r"^- [⬜🔨🧠✅❄️] [AP]\d+\.\d+ · ", t, re.M))
    # LEGACY checkbox Aims are a form the engine supports on purpose
    # (src/common.py aim_progress -> mode="legacy"), and every Section Page of
    # a paper board uses it. Counting only the canonical form printed `aim 0`
    # for all 15 of them (JL 260830). `- [ ] 🗣` is a Decision row and is
    # counted in `dec`, so it is excluded here.
    if not r["aim"]:
        legacy = [m for m in re.findall(r"(?m)^- \[([ xX])\] (\S)", t) if m[1] != "🗣"]
        r["aim"] = len(legacy)
        r["st"] = sum(1 for box, _ in legacy if box.lower() == "x")
    r["dec"] = len(re.findall(r"^- \[[ x]\] 🗣", t, re.M))
    r["law"] = len(re.findall(r"^- (?:\d{6} \w+ · )?[^\s] \*\*", t, re.M))
    r["dia"] = t.count("```text")   # an INLINE ascii block, never a display unit

    # ── evidence/probe/  one folder per question
    cards, seen = [], set()
    for pr in evidence_lane_dirs(pd, "probe"):
        for card in sorted(pr.glob("PP*")):
            if card.name not in seen:
                seen.add(card.name); cards.append(card)
    r["prb"] = len(cards)
    val = read = serves = 0
    for c in cards:
        cm = c / "card.md"
        if not cm.exists():
            continue
        ct = cm.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^state:.*\b(answered|read)\b", ct, re.M | re.I): val += 1
        if re.search(r"^read:\s*✅", ct, re.M): read += 1
        if re.search(r"^serves:", ct, re.M): serves += 1
    r["val"], r["read"], r["srv"] = val, read, serves

    # ── evidence/bibex/  one entry per reference
    ent = ver = 0
    seen_bib = set()
    for bx in evidence_lane_dirs(pd, "bibex"):
        for b in bx.glob("*.bib"):
            if b.name in seen_bib: continue
            seen_bib.add(b.name)
            bt = b.read_text(encoding="utf-8", errors="replace")
            ent += len(re.findall(r"^@\w+\{", bt, re.M))
            ver += len(re.findall(r"verified\s*=", bt))
    r["cit"], r["vfd"] = ent, ver

    # ── evidence/display/  declared/rendered/accepted counts
    dec = ren = acc = frz = 0
    seen_units = set()
    for dp in evidence_lane_dirs(pd, "display"):
        for u in sorted(p for p in dp.iterdir() if p.is_dir()):
            if u.name in seen_units: continue
            seen_units.add(u.name)
            dec += 1
            if (u / "preview.pdf").exists() and any((u / "assets").glob("*")): ren += 1
            rm = u / "README.md"
            if rm.exists() and re.search(r"^accepted:\s*✅", rm.read_text(errors="replace"), re.M): acc += 1
            if (u / "intake" / "inputs").is_dir() and any((u / "intake" / "inputs").iterdir()): frz += 1
    r["dsp"], r["ren"], r["acc"], r["frz"] = dec, ren, acc, frz

    # ── the other plugins, present or absent
    sk = pd / "skill" / f"{pd.name}.md"
    r["skl"] = len(re.findall(r"^- \S", sk.read_text(errors="replace"), re.M)) if sk.exists() else 0
    r["out"] = len(list((pd / "outline").glob("*-outline-v*.md"))) if (pd / "outline").is_dir() else 0
    r["apv"] = 0
    for o in ((pd / "outline").glob("*-outline-v*.md") if (pd / "outline").is_dir() else []):
        if re.search(r"^approved:\s*✅", o.read_text(errors="replace"), re.M): r["apv"] += 1
    r["px"]  = 1 if evidence_lane_dirs(pd, "pagex") else 0
    r["tex"] = 1 if (pd / "latex").is_dir() else 0
    r["doc"] = 1 if (pd / "word").is_dir() else 0
    r["ln"]  = t.count("\n") + 1
    r["state"] = (re.search(r"^state:\s*(\S+)", t, re.M) or [None, "?"])[1]
    r["tick"] = r["apv"] + r["vfd"] + r["read"] + r["acc"]
    return r

COLS = [("page","%-20s"),("ln","%5s"),("state","%-4s"),("div","%4s"),("sub","%4s"),
        ("dia","%4s"),("aim","%4s"),("st","%4s"),("dec","%4s"),("law","%4s"),
        ("out","%4s"),("prb","%4s"),("val","%4s"),("cit","%4s"),("dsp","%4s"),
        ("skl","%4s"),("tick","%5s")]
HEAD = {"page":"page","ln":"lines","state":"st","div":"§","sub":"§.n","dia":"📐",
        "aim":"aim","st":"📍","dec":"🗣","law":"law","out":"🧭","prb":"📮",
        "val":"🔢","cit":"📚","dsp":"🖼","skl":"🛠","tick":"✋"}

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("board", type=Path)
    ap.add_argument("--group", help="one Q/S group id, e.g. QPw")
    ap.add_argument("--md", action="store_true", help="emit a fenced block for a page")
    a = ap.parse_args()
    if not a.board.is_dir():
        print(f"not a board: {a.board}", file=sys.stderr); return 2
    rows = []
    for pid, pd, md in _pages(a.board, a.group):
        r = _count(pd, md); r["page"] = pid; rows.append(r)
    if not rows:
        print("no pages matched", file=sys.stderr); return 1

    line = lambda vals: " ".join(f % str(v) for (k, f), v in zip(COLS, vals))
    head = line([HEAD[k] for k, _ in COLS])
    body = [line([r[k] for k, _ in COLS]) for r in rows]
    tot  = {k: sum(r[k] for r in rows) for k in
            ("ln","div","sub","dia","aim","st","dec","law","out","prb","val","cit","dsp","skl","tick")}
    tot["page"], tot["state"] = f"TOTAL {len(rows)} pages", ""
    foot = line([tot[k] for k, _ in COLS])
    rule = "─" * len(head)

    if a.md: print("```text")
    print(head); print(rule)
    for b in body: print(b)
    print(rule); print(foot)
    print()
    print("§ content divisions · §.n subdivisions · 📐 INLINE ascii diagrams · 📍 State rows")
    print("🗣 Decision Now rows · 🧭 outline files · 📮 probe cards · 🔢 answered cards")
    print("📚 bibex entries · 🖼 DISPLAY UNITS on disk · 🛠 skill rows")
    print("⚠ 📐 and 🖼 are DIFFERENT things.")
    print("   📐 an ascii block inside the markdown. costs nothing, renders as text.")
    print("   🖼 a FOLDER with intake/ recipe/ assets/ that embeds into the pdf.")
    print("   check.py calls the inline block a figure too (division-no-figure at :1071,")
    print("   whose own message at :1076 says diagram). that is the upstream collision.")
    print("✋ human ticks WRITTEN: approved + verified + read + accepted")
    if a.md: print("```")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
