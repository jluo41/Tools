"""Where ONE page sits in the seven-phase page workflow, computed from DISK.

ONE copy of this logic, because two would drift: `cli/pagephase.py` prints the
full strip, `status.py` prints the compact row inside the closing block, and
both call `phase_state()` here. Never writes.

The states, and what each is read from:

    🧭 OUTLINE   the newest outline/<stem>-outline-v<N>.md and its approved: tick
    📮 PROBE     one probe/PP<NN>-*/ per PP id the plan names
    🃏 EVIDENCE  card state: lines · bibex verified= · display preview.pdf + accepted:
    ✏️ DRAFT     the page's own ### content divisions, and whether it postdates the tick
    🖊 REVISE    latex/ present and its newest pdf at least as new as the page (⑥ folded)
    🔍 CHECK     the newest _runs/page/<page>/*.json receipt routed CLOSE

⚠️ `now` is the FIRST phase whose exit test fails, in loop order. That is a
REPORT, never a routing: which phase runs next is decided by authority
(haipipe-page's authority test) and ⑦ CHECK may route anywhere.
"""
import json
import re
from pathlib import Path

MARK = {"done": "✅", "part": "⏳", "owed": "⬜", "hold": "🛑"}

# The phase's own emoji, taken from haipipe-page-workflow §🔁's loop diagram so
# the bar and the diagram teach the same symbol (JL 260820: "I don't like the
# 1, 2, 3, 4 here, it is not that readable, could you change it to be emoji").
# Circled digits render at a few pixels in a terminal font and were unreadable.
#
# ⚠️ ONE deliberate substitution: §🔁 draws ⑦ CHECK as ✅, which is also this
# module's DONE marker, so a bar pairing them reads `✅✅` and says nothing.
# CHECK carries 🔍 here, the act of judging, and only in the bar.
PHASES = (("OUTLINE", "🧭"), ("PROBE", "📮"), ("EVIDENCE", "🃏"),
          ("DRAFT", "✏️"), ("REVISE", "🖊"), ("CHECK", "🔍"))
ORDER = tuple(name for name, _ in PHASES)
EMOJI = dict(PHASES)
# What each phase writes, for the full strip's row labels.
LABEL = {"OUTLINE": "OUTLINE", "PROBE": "PROBE", "EVIDENCE": "EVIDENCE",
         "DRAFT": "DRAFT", "REVISE": "REVISE·COMPILE", "CHECK": "CHECK"}


def _latest_outline(pd):
    od = pd / "outline"
    best, bn = None, 0
    for f in (od.glob("*-outline-v*.md") if od.is_dir() else []):
        m = re.search(r"-outline-v(\d+)\.md$", f.name)
        if m and int(m.group(1)) >= bn:
            best, bn = f, int(m.group(1))
    return best, bn


def _cards(pd):
    pr = pd / "probe"
    rows = []
    for c in sorted(pr.glob("PP*")) if pr.is_dir() else []:
        cm = c / "card.md"
        if not cm.exists():
            continue
        t = cm.read_text(encoding="utf-8", errors="replace")
        rows.append({
            "id": c.name.split("-")[0],
            "state": (re.search(r"^state:\s*(\S+)", t, re.M) or [None, "?"])[1],
            "read": bool(re.search(r"^read:\s*✅", t, re.M)),
            "bound": bool(re.search(r"^target:\s*\S", t, re.M)),
        })
    return rows


def _displays(pd):
    dp = pd / "display"
    rows = []
    for u in sorted(p for p in dp.iterdir() if p.is_dir()) if dp.is_dir() else []:
        rm = u / "README.md"
        inp = u / "intake" / "inputs"
        rows.append({
            "name": u.name,
            "frozen": inp.is_dir() and any(inp.iterdir()),
            "drawn": (u / "preview.pdf").exists(),
            "accepted": rm.exists() and bool(
                re.search(r"^accepted:\s*✅", rm.read_text(errors="replace"), re.M)),
        })
    return rows


def _last_receipt(pd, board=None):
    board = Path(board) if board else pd.parent.parent
    rd = board / "_runs" / "page" / pd.name
    newest = None
    for f in (rd.glob("*.json") if rd.is_dir() else []):
        if newest is None or f.name > newest.name:
            newest = f
    if newest is None:
        return None
    try:
        run = json.loads(newest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    recs = run.get("receipts", [])
    return {"file": newest.name, "last": recs[-1] if recs else None,
            "status": run.get("status")}


def phase_state(page_md, board=None):
    """Return every phase's state plus the counts each one is judged on.

    `page_md` is the page's own markdown file; `board` the board folder, used
    only to find _runs/page/. Returns None when the file is not a page.
    """
    page_md = Path(page_md)
    if not page_md.exists():
        return None
    pd = page_md.parent

    of, ov = _latest_outline(pd)
    approved, marks, pp_ids = False, {"📮": 0, "🧮": 0, "📚": 0, "🖼": 0}, set()
    if of:
        ot = of.read_text(encoding="utf-8", errors="replace")
        approved = bool(re.search(r"^approved:\s*✅", ot, re.M))
        marks = {k: ot.count(k) for k in marks}
        pp_ids = set(re.findall(r"\bPP\d{2}\b", ot))

    cards = _cards(pd)
    missing = sorted(pp_ids - {c["id"] for c in cards})
    answered = [c for c in cards if c["state"].startswith("answered") or c["state"] == "read"]
    blocked = [c for c in cards if c["state"].startswith("blocked")]
    live = [c for c in cards if not c["state"].startswith("blocked")]

    ent = ver = 0
    for b in ((pd / "bibex").glob("*.bib") if (pd / "bibex").is_dir() else []):
        bt = b.read_text(encoding="utf-8", errors="replace")
        ent += len(re.findall(r"^@\w+\{", bt, re.M))
        ver += len(re.findall(r"verified\s*=", bt))

    disp = _displays(pd)
    drawn = [d for d in disp if d["drawn"]]
    acc = [d for d in disp if d["accepted"]]

    page_txt = page_md.read_text(encoding="utf-8", errors="replace")
    divs = len(re.findall(r"^### \d+ · ", page_txt, re.M))
    md_m = page_md.stat().st_mtime
    ap_m = of.stat().st_mtime if of else 0
    tex = pd / "latex"
    pdfs = sorted(tex.rglob("*.pdf")) if tex.is_dir() else []
    pdf_fresh = bool(pdfs) and max(p.stat().st_mtime for p in pdfs) >= md_m

    rec = _last_receipt(pd, board)
    last = rec["last"] if rec else None

    states = {
        "OUTLINE": "done" if approved else ("part" if of else "owed"),
        "PROBE": "owed" if not cards else ("done" if not missing else "part"),
        "EVIDENCE": ("done" if (cards and len(answered) >= len(live)
                                and disp and len(drawn) == len(disp))
                     else ("owed" if not cards and not disp and not ent else "part")),
        "DRAFT": "done" if (divs and md_m >= ap_m) else ("part" if divs else "owed"),
        "REVISE": "done" if pdf_fresh else ("part" if tex.is_dir() else "owed"),
        "CHECK": "done" if (last and last.get("phase") == "CHECK"
                            and last.get("route") == "CLOSE") else "owed",
    }
    read_owed = sum(1 for c in cards if c["state"].startswith("answered") and not c["read"])
    return {
        "page": pd.name, "states": states,
        "now": next((n for n in ORDER if states[n] != "done"), "CLOSE"),
        "outline": {"file": of, "version": ov, "approved": approved, "marks": marks},
        "cards": cards, "missing": missing, "answered": answered, "blocked": blocked,
        "bibex": {"entries": ent, "verified": ver},
        "displays": disp, "drawn": drawn, "accepted": acc,
        "divisions": divs, "page_after_tick": md_m >= ap_m,
        "latex": tex.is_dir(), "pdf_fresh": pdf_fresh,
        "receipt": rec, "last": last,
        "ticks_owed": {
            "approved": 0 if approved else 1, "read": read_owed,
            "verified": max(0, ent - ver), "accepted": len(disp) - len(acc),
        },
    }


def compact(st):
    """One row for the closing status block: where you are, and what is left."""
    bar = " ".join(f"{EMOJI[n]}{MARK[st['states'][n]]}" for n in ORDER)
    owed = sum(st["ticks_owed"].values())
    now = st["now"]
    head = "CLOSE" if now == "CLOSE" else f"{EMOJI[now]} {LABEL[now]}"
    return f"⏱️ {head} · {bar} · ✋{owed}"
