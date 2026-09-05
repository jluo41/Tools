#!/usr/bin/env python3
"""🧮 Values · RECOMPUTE every number a page quotes, and compare (260819).

    python3 checks/values.py [--board DIR ...]

⚠️ KNOWN DEFECT (found 260820, not yet fixed): `RECIPES` below is a fixed,
UNSCOPED dict keyed on bare `PP<NN>.v<n>` strings — built for one Dash-type
page's own board-health metrics (phase/run/lane/audit counts). Every OTHER
page's `PP01.v1`, `PP02.v1`, etc. mean something else entirely (a regression
coefficient, a row count, anything a card names), and they COLLIDE on the same
keys, so this check misapplies the Dash page's recipe to every page's values
and reports 🚨 near-universally on any board with more than that one page.
Confirmed on `02-CMSRegBoard-260725`: every QC page's declared values flagged
🚨 against unrelated board-metric numbers. A real fix reads each card's own
`proof/manifest.yaml`-listed files, not this global dict. Until then: treat
this check's 🚨 output as unreliable outside the page it was built for, and
verify a value by hand against its own card's `proof/` instead.

JL 260819: "I think the machine should check these numbers."

He is right, and it changes what the human tick is FOR. A card whose `bank:` is
`code` answered by READING THE REPO, and a repo read can be read again. Nothing
about comparing 5 to 5 needs a person.

    🤖 the machine owns   is the number still true?
    🧑 the person owns    is this the right number to be asking for?

So `read: ✅` stops meaning "I checked the arithmetic" and starts meaning "I
agree with the judgment inside the question". PP01's `5 phases` is the worked
example: counting the folders is mechanical, and whether COMPILE counts as a
phase at all is not.

Each recomputation below is an evidence item this board actually surveyed, and the
recipe is the one its item row (or its outbound card's `executor/q-executor.md`) names. A value this file cannot
recompute is reported as `unchecked`, never as passing: silence about coverage is
how a green check gets read as a verified page.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
SKILLS = ENGINE.parents[1]
sys.path.insert(0, str(ENGINE))

from src.page_phase import ORDER as PAGE_PHASE_ORDER


# ── the recipes, one per value id ────────────────────────────────────────────
def _phase_census():
    d = SKILLS / "board/page-workflows"
    contracts = [d / f"haipipe-page-{phase.lower()}/SKILL.md"
                 for phase in PAGE_PHASE_ORDER]
    cards = (d / "haipipe-page-workflow/ref/phase-cards.md").read_text(
        encoding="utf-8", errors="replace")
    ticks = re.search(r"(?ms)^## 🧾 Person-reserved ticks, gathered.*?```text\n(.*?)```",
                      cards)
    n_ticks = 0
    if ticks:
        n_ticks = len([l for l in ticks.group(1).splitlines()
                       if l.strip() and not l.lstrip().startswith(("tick", "──"))])
    return {"phases_declared": len(PAGE_PHASE_ORDER),
            "contracts_shipping": sum(path.is_file() for path in contracts),
            "person_reserved_ticks": n_ticks}


def _run_index(board: Path):
    runs = sorted((board / "_runs").rglob("*.json"))
    phases, receipts = set(), 0
    for f in runs:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        r = d.get("receipts") or (d if isinstance(d, list) else [])
        receipts += len(r)
        phases |= {x.get("phase") for x in r if isinstance(x, dict)}
    five = ["CONTEXT", "OUTLINE", "EVIDENCE", "CONTENT", "CHECK"]
    covered = [p for p in five if p in phases]
    return {"runs_total": len(runs), "receipts_total": receipts,
            "coverage": "%d of 5" % len(covered),
            "phases_never_run": len(five) - len(covered)}


def _lane_census(board: Path):
    cards = list(board.rglob("probe/PP*/card.md"))
    planned = read = 0
    for c in cards:
        t = c.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?m)^state:\s*planned\b", t):
            planned += 1
        if re.search(r"(?m)^read:\s*✅", t):
            read += 1
    units = list(board.rglob("display/*/README.md"))
    rendered = sum(1 for u in units if list(u.parent.glob("assets/figure.*")))
    accepted = sum(1 for u in units
                   if re.search(r"(?m)^-?\s*accepted:\s*✅",
                                u.read_text(encoding="utf-8", errors="replace")))
    return {"probe_cards_total": len(cards), "planned": planned,
            "probe_read_ticked": read, "display_rendered": rendered,
            "display_units_total": len(units), "display_accepted": accepted}


def _auditor(board: Path):
    from src.page_lifecycle import audit_run, audit_artifacts
    runs, findings, codes, fails = 0, 0, set(), 0
    for f in sorted((board / "_runs").rglob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        runs += 1
        fs = list(audit_run(d)) + list(audit_artifacts(d, board))
        findings += len(fs)
        codes |= {x.code for x in fs}
        fails += bool(fs)
    return {"runs_audited": runs, "runs_pass": runs - fails,
            "findings_total": findings, "distinct_codes": len(codes),
            "real_violations": sum(1 for c in codes
                                   if c == "checked-version-mismatch")}


# value id -> (recipe key, how to pull the expected number out of the row)
RECIPES = {
    "PP01.v1": ("phase_census", "phases_declared"),
    "PP01.v2": ("phase_census", "contracts_shipping"),
    "PP01.v3": ("phase_census", "person_reserved_ticks"),
    "PP02.v1": ("run_index", "runs_total"),
    "PP02.v2": ("run_index", "receipts_total"),
    "PP02.v3": ("run_index", "coverage"),
    "PP02.v4": ("run_index", "phases_never_run"),
    "PP03.v1": ("lane_census", "probe_cards_total"),
    "PP03.v2": ("lane_census", "planned"),
    "PP03.v3": ("lane_census", "probe_read_ticked"),
    "PP03.v4": ("lane_census", "display_rendered"),
    "PP03.v5": ("lane_census", "display_accepted"),
    "PP04.v1": ("auditor", "runs_audited"),
    "PP04.v2": ("auditor", "runs_pass"),
    "PP04.v3": ("auditor", "findings_total"),
    "PP04.v4": ("auditor", "distinct_codes"),
    "PP04.v5": ("auditor", "real_violations"),
}

_ROW = re.compile(r"^-\s*(v\d+)\s*·\s*(.+?)\s*·\s*(.+?)\s*(?:·\s*(.+?))?\s*$", re.M)


def _first_int(s):
    m = re.search(r"-?\d+", str(s))
    return int(m.group(0)) if m else None


def sweep(board: Path):
    """-> (rows, unchecked) · one row per declared value."""
    recipes = {}
    rows, unchecked = [], []
    for card in sorted(board.rglob("probe/PP*/card.md")):
        pid = card.parent.name.split("-")[0]
        txt = card.read_text(encoding="utf-8", errors="replace")
        blk = re.search(r"(?ms)^##\s+Values\s*$(.*?)(?=^##\s|\Z)", txt)
        if not blk:
            continue
        for vid, what, num, _src in _ROW.findall(blk.group(1)):
            key = "%s.%s" % (pid, vid)
            if key not in RECIPES:
                unchecked.append((key, what.strip()))
                continue
            recipe, field = RECIPES[key]
            if recipe not in recipes:
                recipes[recipe] = {"phase_census": _phase_census,
                                   "run_index": lambda: _run_index(board),
                                   "lane_census": lambda: _lane_census(board),
                                   "auditor": lambda: _auditor(board)}[recipe]()
            got, want = recipes[recipe][field], num.strip()
            ok = (str(got) == want) or (_first_int(got) is not None
                                        and _first_int(got) == _first_int(want))
            rows.append((key, what.strip(), want, got, ok))
    return rows, unchecked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", nargs="*", default=None)
    args = ap.parse_args()
    boards = [Path(b) for b in args.board] if args.board else \
        sorted(p for p in (SKILLS / "diagrams").iterdir() if (p / "_runs").is_dir())

    bad = []
    for b in boards:
        rows, unchecked = sweep(b)
        if not rows and not unchecked:
            continue
        print("📋 %s" % b.name)
        for key, what, want, got, ok in rows:
            print("   %s %-9s %-32s quoted %-9s disk %s"
                  % ("✅" if ok else "🚨", key, what[:32], want, got))
            if not ok:
                bad.append("%s: page quotes %r, disk says %r" % (key, want, got))
        for key, what in unchecked:
            print("   ⬜ %-9s %-32s no recipe: a person owns this one"
                  % (key, what[:32]))
        print("   %d recomputed · %d unchecked" % (len(rows), len(unchecked)))

    print()
    if bad:
        print("🚨 %d value(s) no longer match the repo" % len(bad))
        for x in bad:
            print("   ", x)
        return 1
    print("✅ every recomputable value still matches the repo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
