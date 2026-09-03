"""Where ONE page sits in the seven-phase page workflow, computed from DISK.

ONE copy of this logic, because two would drift: `cli/pagephase.py` prints the
full strip, `status.py` prints the compact row inside the closing block, and
both call `phase_state()` here. Never writes.

The states, and what each is read from:

    🧭 OUTLINE   the newest outline/<stem>-outline-v<N>.md and its approved: tick
                 (SHAPE), plus the Evidence Item table's Decide per item (SURVEY)
    🃏 EVIDENCE  the Evidence Item table joined to local Results: ready · folded (LAND,
                 EMBED); legacy pages without a table: card state: lines ·
                 bibex verified= · display preview.pdf + accepted:
    ✏️ DRAFT     the page's own ### content divisions, and whether it postdates the tick
    🖊 REVISE    delivery/latex/ present and its newest pdf at least as new as the page (⑥ folded)
    🔍 CHECK     the newest _runs/page/<page>/*.json receipt routed CLOSE

⚠️ `now` is the FIRST phase whose exit test fails, in loop order. That is a
REPORT, never a routing: which phase runs next is decided by authority
(haipipe-page's authority test) and CHECK may route anywhere.
"""
import json
import re
from pathlib import Path

from src import item_table

from .common import delivery_lane_dirs, evidence_lane_dirs
from .folder_contract import (
    current_folder_kind,
    resolve as resolve_folder_contract,
)


SKILLS_ROOT = Path(__file__).resolve().parents[3]

MARK = {"done": "✅", "part": "⏳", "owed": "⬜", "hold": "🛑"}

# ── THE OWED LEDGER ──────────────────────────────────────────────────────
# `ticks_owed` has always carried the COUNT. The count tells a person there is
# a debt; it never tells them where to spend the one act that is theirs. So
# `owed_ledger()` below returns the LIST, and each row carries the machine's
# half beside the human's, which is what makes one artifact serve both modes:
#
#   🧑 copilot   you watch the list shrink and answer as you go
#   🤖 auto      the run does not stop; the list is what you are handed at the end
#
# `QPw00g-human-gate`'s open ruling was "no surface joins the owed ticks". This
# is that join. It is a REPORT: it writes nothing and ticks nothing. The list is
# intentionally variable: a phase-owned Folder may declare that it owes no
# Page-local RULING because its domain gate owns the closure decision.
#
# What each row ASKS is quoted from the matching rules file's `🚫 NOT rules`
# section — the questions an agent is forbidden to answer because they are
# re-made every time. This dict is a POINTER to those files, never a copy of
# the rules themselves (approve-rules/README.md owns the 🤖/🧑 cut).
HUMAN_ASKS = {
    "approved": "is this the DIRECTION I want, and is this round worth doing now?",
    "read":     "was this the right question to ask the bank, and what does the number MEAN here?",
    "verified": "is this the right literature to stand this claim on?",
    "accepted": "is this display good overall, and is it the right kind for the argument?",
    "ruling":   "the Folder owner's declared closing question — who may decide it, and where?",
}
# The agent-side rules file for each tick, or None where none exists BY DESIGN.
RULES_FILE = {
    "approved": "approve-rules.md", "read": "value-rules.md",
    "verified": "cite-rules.md", "accepted": "display-rules.md",
    "ruling": None,
}
_CHECKED_RE = re.compile(r"^checked\s*[:=]\s*(.+?)\s*$", re.M)


def _checked(text):
    """The agent half, if an approver has run: `checked: ✅ auto <YYMMDD> · …`.

    Two syntaxes because the host decides: `key: value` on a card, an outline
    and a display README, `key = {value}` inside a bibtex entry
    (approve-rules/README.md § What a pass looks like).
    """
    m = _CHECKED_RE.search(text or "")
    return m.group(1).strip().strip("{}").strip() if m else None

# The phase's own emoji, taken from haipipe-page-workflow §🔁's loop diagram so
# the bar and the diagram teach the same symbol (JL 260820: "I don't like the
# 1, 2, 3, 4 here, it is not that readable, could you change it to be emoji").
# Circled digits render at a few pixels in a terminal font and were unreadable.
#
# ⚠️ ONE deliberate substitution: the loop draws CHECK as ✅, which is also this
# module's DONE marker, so a bar pairing them reads `✅✅` and says nothing.
# CHECK carries 🔍 here, the act of judging, and only in the bar.
PHASES = (("OUTLINE", "🧭"), ("EVIDENCE", "🃏"),
          ("DRAFT", "✏️"), ("REVISE", "🖊"), ("CHECK", "🔍"))
ORDER = tuple(name for name, _ in PHASES)
EMOJI = dict(PHASES)
LABEL = {"OUTLINE": "OUTLINE", "EVIDENCE": "EVIDENCE",
         "DRAFT": "DRAFT", "REVISE": "REVISE·COMPILE", "CHECK": "CHECK"}
# the cycle words of the OUTLINE part live on the item table (src/item_table.py)


def _latest_outline(pd):
    od = pd / "outline"
    best, bn = None, 0
    for f in (od.glob("*-outline-v*.md") if od.is_dir() else []):
        m = re.search(r"-outline-v(\d+)\.md$", f.name)
        if m and int(m.group(1)) >= bn:
            best, bn = f, int(m.group(1))
    return best, bn


def _cards(pd):
    rows = []
    seen = set()
    # Canonical Folder-native evidence lane first. The flat lane remains
    # readable so stored pre-migration Pages do not disappear from reports.
    for pr in evidence_lane_dirs(pd, "probe"):
        for c in sorted(pr.glob("PP*")) if pr.is_dir() else []:
            if c.name in seen:
                continue
            seen.add(c.name)
            cm = c / "card.md"
            if not cm.exists():
                continue
            t = cm.read_text(encoding="utf-8", errors="replace")
            rows.append({
                "id": c.name.split("-")[0],
                "state": (re.search(r"^state:\s*(\S+)", t, re.M) or [None, "?"])[1],
                "read": bool(re.search(r"^read:\s*✅", t, re.M)),
                "bound": bool(re.search(r"^target:\s*\S", t, re.M)),
                "path": cm, "checked": _checked(t),
            })
    return rows


def _displays(pd):
    rows = []
    seen = set()
    for dp in evidence_lane_dirs(pd, "display"):
        for u in sorted(p for p in dp.iterdir() if p.is_dir()):
            if u.name in seen:
                continue
            seen.add(u.name)
            rm = u / "README.md"
            inp = u / "intake" / "inputs"
            rt = rm.read_text(errors="replace") if rm.exists() else ""
            rows.append({
                "name": u.name,
                "frozen": inp.is_dir() and any(inp.iterdir()),
                "drawn": (u / "preview.pdf").exists(),
                "accepted": bool(re.search(r"^accepted:\s*✅", rt, re.M)),
                "path": rm, "checked": _checked(rt),
            })
    return rows


def _bibex(pd):
    """One row per bibtex ENTRY, because a count cannot be spent.

    `verified` is a person's (cite-rules, and haipipe-plugin-evidence rules it
    260815); `checked` is the approver's R1-R7 pass. An entry carrying
    `verified = {}` is EXPLICITLY unverified — cite-rules R7 — so an empty
    brace reads as owed, never as done.
    """
    rows = []
    seen = set()
    for bx in evidence_lane_dirs(pd, "bibex"):
        for b in sorted(bx.glob("*.bib")):
            if b.name in seen:
                continue
            seen.add(b.name)
            bt = b.read_text(encoding="utf-8", errors="replace")
            for chunk in re.split(r"(?m)^(?=@)", bt):
                m = re.match(r"@\w+\{\s*([^,\s]+)", chunk)
                if not m:
                    continue
                v = re.search(r"verified\s*=\s*\{([^}]*)\}", chunk)
                rows.append({"key": m.group(1), "file": b,
                             "verified": bool(v and v.group(1).strip()),
                             "checked": _checked(chunk)})
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
    outline_checked = None
    if of:
        ot = of.read_text(encoding="utf-8", errors="replace")
        approved = bool(re.search(r"^approved:\s*✅", ot, re.M))
        outline_checked = _checked(ot)
        marks = {k: ot.count(k) for k in marks}
        pp_ids = set(re.findall(r"\bPP\d{2}\b", ot))

    cards = _cards(pd)
    missing = sorted(pp_ids - {c["id"] for c in cards})
    answered = [c for c in cards if c["state"].startswith("answered") or c["state"] == "read"]
    blocked = [c for c in cards if c["state"].startswith("blocked")]
    live = [c for c in cards if not c["state"].startswith("blocked")]

    bib = _bibex(pd)
    # The counts stay exactly as they were: `ent` is every entry, `ver` every
    # entry carrying a NON-EMPTY verified (cite-rules R7's `verified = {}` is
    # the explicit unverified form and must not count as done).
    ent, ver = len(bib), sum(1 for e in bib if e["verified"])

    disp = _displays(pd)
    drawn = [d for d in disp if d["drawn"]]
    acc = [d for d in disp if d["accepted"]]

    page_txt = page_md.read_text(encoding="utf-8", errors="replace")
    frontmatter_folder_kind = (
        re.search(r"^folder-kind:\s*([a-z][a-z0-9-]*)\s*$", page_txt, re.M)
        or [None, ""]
    )[1]
    legacy_page_type = (re.search(r"^page-type:\s*([a-z][a-z0-9-]*)\s*$",
                                  page_txt, re.M) or [None, ""])[1]
    # Existing Pages without a phase-owned Folder identity keep the historical
    # conservative default: they owe a local RULING until CHECK closes. A
    # phase contract may explicitly remove that debt or bind it to its domain
    # gate. Ambiguity must never silently waive a human-owned decision.
    owner_ruling = "legacy-default"
    owner_ruling_required = True
    owner_ruling_error = ""
    folder_kind = frontmatter_folder_kind
    folder_kind_source = "frontmatter" if folder_kind else ""
    try:
        phase_folder_kind = current_folder_kind(pd)
        if phase_folder_kind:
            page_folder_kind = folder_kind
            folder_kind = phase_folder_kind
            folder_kind_source = "workflow/phase.yaml"
            if page_folder_kind and page_folder_kind != phase_folder_kind:
                raise ValueError(
                    "workflow/phase.yaml current.folder-kind "
                    f"{phase_folder_kind!r} conflicts with Page frontmatter "
                    f"folder-kind {page_folder_kind!r}"
                )
        folder_contract = resolve_folder_contract(
            SKILLS_ROOT, folder_kind=folder_kind,
            legacy_page_type=legacy_page_type,
        )
    except ValueError as exc:
        folder_contract = None
        owner_ruling = "ambiguous"
        owner_ruling_error = str(exc)
    if folder_contract is not None:
        owner_ruling = folder_contract.page_ruling
        owner_ruling_required = owner_ruling != "none"
    divs = len(re.findall(r"^### \d+ · ", page_txt, re.M))
    md_m = page_md.stat().st_mtime
    ap_m = of.stat().st_mtime if of else 0
    tex_dirs = delivery_lane_dirs(pd, "latex")
    pdfs = sorted(p for tex in tex_dirs for p in tex.rglob("*.pdf"))
    pdf_fresh = bool(pdfs) and max(p.stat().st_mtime for p in pdfs) >= md_m

    rec = _last_receipt(pd, board)
    last = rec["last"] if rec else None

    # The Evidence Item table: SHAPE's typed contracts, SURVEY's Run graphs,
    # and LAND's local Result pointers. A page with no typed table keeps the
    # legacy lane-based reading below during migration.
    items = item_table.summarize(page_md, of) if of else None
    has_table = bool(items and items["rows"])
    ic = items["counts"] if items else {}
    live_rows = (items["marks"] - ic.get("deferred", 0) - ic.get("dropped", 0)) if items else 0
    folded_rows = ic.get("folded", 0) + ic.get("accepted", 0)

    states = {
        "OUTLINE": ("done" if approved and (not has_table or items["decided"] == items["rows"])
                    else ("part" if of else "owed")),
        "EVIDENCE": ((("done" if live_rows and folded_rows >= live_rows
                       else ("owed" if not ic.get("planned") and not ic.get("ready") and not folded_rows
                             else "part")) if has_table else
                     ("done" if (cards and len(answered) >= len(live)
                                 and disp and len(drawn) == len(disp))
                      else ("owed" if not cards and not disp and not ent else "part")))),
        "DRAFT": "done" if (divs and md_m >= ap_m) else ("part" if divs else "owed"),
        "REVISE": "done" if pdf_fresh else ("part" if tex_dirs else "owed"),
        "CHECK": "done" if (last and last.get("phase") == "CHECK"
                            and last.get("route") == "CLOSE") else "owed",
    }
    read_owed = sum(1 for c in cards if c["state"].startswith("answered") and not c["read"])
    return {
        "page": pd.name, "states": states,
        "now": next((n for n in ORDER if states[n] != "done"), "CLOSE"),
        "outline": {"file": of, "version": ov, "approved": approved,
                    "marks": marks, "checked": outline_checked},
        "items": items, "cycle": items["cycle"] if items else ("SHAPE" if of else "SHAPE"),
        "cards": cards, "missing": missing, "answered": answered, "blocked": blocked,
        "bibex": {"entries": ent, "verified": ver, "rows": bib},
        "displays": disp, "drawn": drawn, "accepted": acc,
        "divisions": divs, "page_after_tick": md_m >= ap_m,
        "latex": tex.is_dir(), "pdf_fresh": pdf_fresh,
        "receipt": rec, "last": last, "dir": pd,
        # The page's OWN words about what it still owes. The RULING is the one
        # tick with no rules file (approve-rules/README.md, on purpose), so the
        # ledger reports this line verbatim rather than inventing a check.
        "state_line": (re.search(r"^state:\s*(.+)$", page_txt, re.M)
                       or [None, ""])[1].strip(),
        # The ledger is variable. Four plugin ticks are artifact-driven; the
        # owner RULING is phase-driven. Legacy Pages conservatively owe it,
        # while a phase contract may say `none` or reuse its domain gate.
        # `sum(ticks_owed.values()) == len(owed_ledger(st))` remains invariant.
        "ticks_owed": {
            "approved": 0 if approved else 1, "read": read_owed,
            "verified": max(0, ent - ver),
            "accepted": sum(1 for d in disp if d["drawn"] and not d["accepted"]),
            "ruling": 0 if states["CHECK"] == "done" or not owner_ruling_required else 1,
        },
        "owner_ruling": owner_ruling,
        "owner_ruling_required": owner_ruling_required,
        "owner_ruling_error": owner_ruling_error,
        "folder_kind": folder_kind,
        "folder_kind_source": folder_kind_source,
    }


def owed_ledger(st):
    """Every human tick this page still owes, as ROWS — the join `QPw00g` asks for.

    One row per act a person still has to perform, each carrying the machine's
    half beside it so the person can see what was already established and spend
    their attention on what was not. Reads only; writes and ticks nothing.

    Row keys: tick · where (short path) · note (why it is owed) · checked (the
    approver's pass, or None) · rules (its rules file, or None) · ask (what the
    person is being asked to judge).
    """
    pd = st["dir"]
    rel = lambda f: str(Path(f).relative_to(pd)) if f else "—"
    row = lambda tick, where, note, checked: {
        "tick": tick, "where": where, "note": note, "checked": checked,
        "rules": RULES_FILE[tick], "ask": HUMAN_ASKS[tick]}
    out = []

    # ① the plan. Owed from the moment an outline file exists.
    o = st["outline"]
    if not o["approved"]:
        out.append(row("approved", rel(o["file"]) if o["file"] else "outline/ (none yet)",
                       f"v{o['version']}" if o["file"] else "no outline written yet",
                       o["checked"]))

    # ③v every ANSWERED card nobody has read. A card still in flight owes
    # nothing yet: `read:` is the acceptance of an answer, not of a question.
    for c in st["cards"]:
        if c["state"].startswith("answered") and not c["read"]:
            out.append(row("read", rel(c["path"]), f"{c['id']} · {c['state']}", c["checked"]))

    # ③c every bibtex entry without a person's `verified`. cite-rules R7: an
    # empty `verified = {}` is the EXPLICIT unverified form, so it lands here.
    for e in st["bibex"]["rows"]:
        if not e["verified"]:
            out.append(row("verified", f"{rel(e['file'])} · {e['key']}",
                           "entry landed, unverified", e["checked"]))

    # ③d every DRAWN unit nobody has accepted. An undrawn unit owes a render
    # first, which is EVIDENCE's machine work and not a person's act.
    for d in st["displays"]:
        if d["drawn"] and not d["accepted"]:
            out.append(row("accepted", rel(d["path"]), f"{d['name']} · drawn", d["checked"]))

    # The owner RULING is last and deliberately uncheckable. Whether it exists
    # comes from the owning workflow phase, not from the generic Page loop.
    if st["ticks_owed"]["ruling"]:
        out.append(row("ruling", f"{st['page']}.md",
                       f"{st['state_line'] or 'no state: line'} · "
                       f"owner: {st['owner_ruling']}", None))
    return out


def render_ledger(st, width=78):
    """The ledger as text. `cli/pagephase.py --owed` prints this."""
    rows = owed_ledger(st)
    if not rows:
        return ["✋ nothing owed — every human tick on this page is ticked."]
    L = [f"✋ {len(rows)} human tick{'s' if len(rows) != 1 else ''} owed on {st['page']}",
         "   (a machine may never write one of these — approve-rules R10)"]
    for i, r in enumerate(rows, 1):
        L.append("")
        L.append(f"{i:>2}. 🧑 {r['tick']:<9s} {r['where']}")
        L.append(f"      {r['note']}")
        if r["rules"] is None:
            L.append("      🤖 no rules file, by design — nothing was pre-checked")
        elif r["checked"]:
            L.append(f"      🤖 checked: {r['checked']}")
        else:
            L.append(f"      🤖 not checked yet · {r['rules']} has never run here")
        L.append(f"      ❓ {r['ask']}")
    return L


def compact(st):
    """One row for the closing status block: where you are, and what is left."""
    bar = " ".join(f"{EMOJI[n]}{MARK[st['states'][n]]}" for n in ORDER)
    owed = sum(st["ticks_owed"].values())
    now = st["now"]
    head = "CLOSE" if now == "CLOSE" else f"{EMOJI[now]} {LABEL[now]}"
    return f"⏱️ {head} · {bar} · ✋{owed}"
