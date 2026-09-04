#!/usr/bin/env python3
"""Roll a stage's units up onto the control page that already sits above them.

WHY. Ask "how are the claims doing" and today you open four pages and hold
four state lines in your head. The facts are on disk, one per unit, and nothing
adds them up, so the answer exists and is invisible. That is the same failure as
a number that lives only in prose, and it is the failure this closes.

WHAT A GROUP IS, read off the filenames rather than declared anywhere:

    S-Work-C-claims          the CONTROL page: family Work, kind C, no unit number
    S-Work-C0 … S-Work-C3    its units
    S-Appendix-0-control     a control page may also be unit 0
    S-<Family>-Dash          or it may be named Dash

The grouping is by KIND, not by folder, because `S02-work` holds three kinds and
the question a person has is about claims, never about the folder. Measured on
the MISQ board: eight stages hold more than one unit and four of them carry no
roll-up at all, so the coverage was accidental rather than decided.

    python3 dash.py <board-dir>              print every group's roll-up
    python3 dash.py <board-dir> --write      write each into its control page
    python3 dash.py <board-dir> --json       the same data for anything else

Each block carries a MEASURED date and a regenerate command, which is what
`check.py`'s `generated-block-stale` rule reads. A roll-up never completes, so
freshness is the only honesty it can offer.
"""
import json
import pathlib
import re
import sys
from collections import defaultdict
from datetime import datetime

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from src.common import aim_progress                              # noqa: E402

# One marker pair PER GENERATOR. A shared pair means the last writer
# silently deletes every other block on the page, which is what a shared
# `form:` pair did on 260806 before this line existed.
BEGIN, END = ("# --- units:begin (generated) ---",
              "# --- units:end ---")
# S-Work-C3-context  ->  family Work · kind C · unit 3
# S-Work-C-claims    ->  family Work · kind C · unit ''   (the control page)
# S-Appendix-0-…     ->  family Appendix · kind '' · unit 0
NAME = re.compile(r"^S-([A-Za-z]+)-([A-Za-z]*)(\d*)(?:-(.*))?\.md$")
SKIP_DIR = ("/board/", "/_archive/", "/_old/", "/workspace/")


def section(text, *names):
    for n in names:
        m = re.search(rf"(?ms)^##\s+{n}\s*$\n?(.*?)(?=^##\s+|\Z)", text)
        if m:
            return m.group(1)
    return ""


def parse_name(name):
    """`S-Work-C3-context.md` -> ('Work', 'C3'). The token after the family."""
    bits = name[:-3].split("-")
    if len(bits) < 3 or bits[0] != "S":
        return None, None
    return bits[1], bits[2]


TOKEN = re.compile(r"^([A-Za-z]*)(\d*)([a-z0-9]*)$")


def groups(board):
    """Every (family, kind) group, control page and units apart.

    The hard part is that one shape carries two meanings. In `S02-work` the
    token `C` is the CONTROL page for claims and `C0`-`C3` are its units; in
    `S07-appendix` the token `A` is appendix A, a UNIT, and nothing is named
    `A0`. Reading a bare letter as a control page either way drops six appendix
    units on the floor, which is exactly what the first version of this did.

    So the rule is relational rather than lexical: a bare letter is a control
    page ONLY IF numbered siblings carry the same letter. Otherwise it is a
    unit, and the family's control page is the one named `0` or `Dash`.
    """
    by_family = defaultdict(list)
    for p in sorted(board.rglob("S-*.md")):
        if any(x in str(p) for x in SKIP_DIR):
            continue
        family, token = parse_name(p.name)
        if family:
            by_family[family].append((token, p))

    found = {}
    for family, members in by_family.items():
        # which bare letters have numbered siblings: those letters are kinds
        kinds = {TOKEN.match(t).group(1) for t, _ in members
                 if TOKEN.match(t) and TOKEN.match(t).group(1)
                 and TOKEN.match(t).group(2)}
        for token, p in members:
            m = TOKEN.match(token)
            letter, num = (m.group(1), m.group(2)) if m else (token, "")
            kind = letter if letter in kinds else ""
            g = found.setdefault((family, kind), dict(control=None, units=[]))
            control = (token.lower() == "dash"
                       or (letter in kinds and not num)          # `C` above C0-C3
                       or (not kind and token == "0"))           # `0` above A-F
            (g.__setitem__("control", p) if control else g["units"].append(p))
    return {k: v for k, v in found.items() if len(v["units"]) > 1}


def measure(page):
    """The two facts every unit page carries, whatever its type."""
    t = page.read_text(errors="ignore")
    state = re.search(r"(?m)^state:\s*(.+)$", t)
    aims = section(t, "Aims", "Done when", "Items to Finish")
    prog = aim_progress(aims, section(t, "States", "Now", "Where we are"))
    title = re.search(r"(?m)^#\s+(.+)$", t)
    return dict(
        page_id=re.sub(r"^(S-[A-Za-z]+-[A-Za-z]*\d*).*$", r"\1", page.stem),
        file=page.name,
        state=(state.group(1).strip() if state else "?"),
        met=prog["met"], total=prog["total"], mode=prog["mode"],
        title=(title.group(1).strip() if title else page.stem),
    )


def render(family, kind, control, units, date, board_name):
    rows = [measure(u) for u in units]
    done = sum(1 for r in rows if r["state"].split()[0] in ("✅", "⏸"))
    aims_met = sum(r["met"] for r in rows)
    aims_tot = sum(r["total"] for r in rows)
    W = 76
    L = [BEGIN,
         f"  {family.upper()}{(' · ' + kind) if kind else ''} UNIT ROLL-UP, "
         f"MEASURED {date}. GENERATED; do not hand-edit.",
         f"  regenerate: dash.py {board_name} --write",
         "  state is each unit's own line · aims are met of declared, read off States",
         "",
         f"  {'unit':<16}{'state':<34}{'aims':>7}   what it carries",
         "  " + "-" * W]
    for r in rows:
        st = r["state"][:32]
        aim = f"{r['met']}/{r['total']}" if r["total"] else "-"
        what = re.sub(r"^S [A-Za-z]+ \S+ · ", "", r["title"])[:30]
        L.append(f"  {r['page_id']:<16}{st:<34}{aim:>7}   {what}")
    L += ["  " + "-" * W,
          f"  {len(rows)} units · {done} at a closed state · "
          f"{aims_met} of {aims_tot} declared aims met"]
    if aims_tot and not aims_met:
        # The diagnosis differs by which Aim vocabulary the units use, and
        # saying the wrong one sends a reader to the wrong file. A legacy page
        # keeps its state in the checkbox, so zero met means zero ticked, full
        # stop. A canonical page reads its state out of States, so zero met can
        # also mean nobody wrote that section.
        legacy = sum(1 for r in rows if r["mode"] == "legacy")
        why = ("every unit still uses checkbox Aims, so this is simply nothing "
               "ticked" if legacy == len(rows) else
               "read off States, so it is either true or a States section "
               "nobody wrote")
        L.append(f"  no aim is met on any unit: {why}")
    L.append(END)
    return "\n".join(L), rows


def write_into(control, block):
    """Replace the block, or insert it under Outline the first time."""
    t = control.read_text(encoding="utf-8")
    if BEGIN in t:
        head, rest = t.split(BEGIN, 1)
        return head + block + rest.split(END, 1)[1], "replaced"
    anchor = (re.search(r"(?m)^## (?:Outline|Diagram)\s*$", t)
              or re.search(r"(?m)^## Content\s*$", t))
    if not anchor:
        return None, "no ## Outline or ## Content to insert under"
    lead = ("\n\n**Where its units stand**: measured from the unit pages, "
            "never typed.\n\n")
    return (t[:anchor.end()] + lead + "```text\n" + block + "\n```\n"
            + t[anchor.end():]), "inserted"


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    board = pathlib.Path(args[0]).resolve()
    # Default to the REAL clock, not to "unknown date". The standing rule is
    # never to invent a date, and reading one is the opposite of inventing it.
    # A roll-up whose header says when it was measured, printing "unknown
    # date", is the stale-aggregate failure these blocks exist to prevent.
    date = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--date=")),
                datetime.now().strftime("%y%m%d"))
    out = {}
    for (family, kind), g in sorted(groups(board).items()):
        block, rows = render(family, kind, g["control"], g["units"], date, board.name)
        label = f"{family}{('-' + kind) if kind else ''}"
        out[label] = dict(control=g["control"].name if g["control"] else None,
                          units=rows)
        if "--json" in sys.argv:
            continue
        if "--write" in sys.argv:
            if not g["control"]:
                print(f"  ⚠️  {label:<14} {len(rows)} units and NO control page to "
                      "carry the roll-up")
                continue
            new, how = write_into(g["control"], block)
            if new is None:
                print(f"  ⚠️  {label:<14} {how}")
                continue
            g["control"].write_text(new, encoding="utf-8")
            print(f"  ✅ {label:<14} {len(rows)} units -> {g['control'].name} ({how})")
        else:
            print(block + "\n")
    if "--json" in sys.argv:
        print(json.dumps(dict(measured=date, board=board.name, groups=out), indent=2))
