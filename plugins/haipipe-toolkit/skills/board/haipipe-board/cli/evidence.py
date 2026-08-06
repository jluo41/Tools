#!/usr/bin/env python3
"""Roll up every evidence topic on a board: what was asked, what came back.

WHY THIS EXISTS. The question a person actually has is not "what type is this
page", it is "how far along is the evidence": how many literature topics are
still out, whether a value's answer has landed, whether the consumers who asked
for it ever wrote it down. Every fact needed to answer that is already on disk
and machine-readable, in the `### E<n>` divisions and the QA records below
`QA-probe/`, and nothing computed it. So the state was true and invisible, which
is the same failure as a number that lives only in prose.

Run it on the MISQ board the day it was written and the answer arrives in one
screen: 28 conversations, 11 answered, and 68 consumer rows of which zero were
ever closed. Answers had been coming back for weeks and not one had been written
back to the row that asked.

    python3 evidence.py <board-dir>            print the roll-up
    python3 evidence.py <board-dir> --block    print it as a generated block,
                                               ready for a control page
    python3 evidence.py <board-dir> --json     the same data, for anything else

The block form carries a MEASURED date and a regenerate command, which is what
`check.py`'s `generated-block-stale` rule reads. A roll-up has no completion, so
freshness is the only honesty it can offer.
"""
import json
import pathlib
import re
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from src.topic_entry_contract import PROBE_DIRS, head            # noqa: E402

BEGIN, END = "# --- form:begin (generated) ---", "# --- form:end ---"
E_DIV = re.compile(r"^### (E\d+) · (.+?)\s*$", re.M)
POINTER = re.compile(r"🔗 QA-probe:\s*`?([^`\s·]+)`?.*?state:\s*([a-z-]+)")
# A consumer row leads with its state marker, which is the one thing that says
# whether the answer reached the sentence that asked for it.
CONSUMER = re.compile(r"^\s*[-*]\s*(⬜|✅|🔨|🧠|❄️?)\s", re.M)
ROUTE = re.compile(r"(?m)^route:\s*(outward|inward)\s*$")

# Read is the answer landing in the paper; answered-local is the answer being
# produced here. Both mean the question is no longer out.
LANDED = {"read", "answered-local"}


def section(text, name):
    m = re.search(rf"(?ms)^##\s+{name}\s*$\n?(.*?)(?=^##\s+|\Z)", text)
    return m.group(1) if m else ""


def topics(board):
    """Every evidence page on the board, with its divisions and their states."""
    out = []
    for page in sorted(board.rglob("*.md")):
        s = str(page)
        if any(x in s for x in ("/board/", "/_archive/", "/_old/")):
            continue
        if any(d in page.parts for d in PROBE_DIRS):
            continue
        text = page.read_text(errors="ignore")
        route = ROUTE.search(head(text))
        if not route:
            continue
        content = section(text, "Content")
        divisions = []
        for name, question in E_DIV.findall(content):
            body = content.split(f"### {name} · ", 1)[1].split("\n### ", 1)[0]
            hit = POINTER.search(body)
            divisions.append(dict(
                division=name,
                question=question.strip(),
                record=hit.group(1) if hit else "",
                state=hit.group(2) if hit else ("queue" if name == "E0" else "unbound"),
                consumers=Counter(CONSUMER.findall(body)),
            ))
        out.append(dict(page=page.name, route=route.group(1),
                        stage=page.parent.name, divisions=divisions))
    return out


def rollup(pages):
    rows, tot = [], Counter()
    for p in pages:
        real = [d for d in p["divisions"] if d["division"] != "E0"]
        st = Counter(d["state"] for d in real)
        cons = Counter()
        for d in real:
            cons.update(d["consumers"])
        queued = sum(len(d["consumers"]) for d in p["divisions"]
                     if d["division"] == "E0")
        rows.append(dict(page=p["page"], route=p["route"], asked=len(real),
                         landed=sum(st[s] for s in LANDED), states=dict(st),
                         consumers=sum(cons.values()),
                         closed=cons.get("✅", 0), waiting=cons.get("⬜", 0),
                         incoming=queued))
        tot["asked"] += len(real)
        tot["landed"] += sum(st[s] for s in LANDED)
        tot["consumers"] += sum(cons.values())
        tot["closed"] += cons.get("✅", 0)
        tot["incoming"] += queued
    return rows, tot


def render(rows, tot, date, board_name):
    W = 74
    L = [BEGIN,
         f"  EVIDENCE ROLL-UP, MEASURED {date}. GENERATED; do not hand-edit.",
         f"  regenerate: evidence.py {board_name} --block",
         "  asked = E divisions · landed = answer read or produced here",
         "  closed = consumer rows whose answer reached the sentence that asked",
         "",
         f"  {'topic':<38}{'route':<9}{'asked':>6}{'landed':>7}{'cons':>6}{'closed':>7}",
         "  " + "-" * W]
    for r in rows:
        flag = "" if r["closed"] == r["consumers"] else "  !"
        L.append(f"  {r['page'][:-3]:<38}{r['route']:<9}{r['asked']:>6}"
                 f"{r['landed']:>7}{r['consumers']:>6}{r['closed']:>7}{flag}")
    L += ["  " + "-" * W,
          f"  {tot['asked']} conversations · {tot['landed']} answered · "
          f"{tot['asked'] - tot['landed']} still out",
          f"  {tot['consumers']} consumer rows · {tot['closed']} closed · "
          f"{tot['consumers'] - tot['closed']} waiting on a write-back"]
    if tot["incoming"]:
        L.append(f"  {tot['incoming']} question(s) sitting in an E0 incoming queue")
    if tot["consumers"] and not tot["closed"]:
        L += ["",
              "  NOT ONE consumer row is closed. An answer that came back and was",
              "  never written to the row that asked for it is the quiet failure",
              "  this table exists to make loud: the page reads answered and the",
              "  sentence that needed it still has nothing."]
    L.append(END)
    return "\n".join(L)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    board = pathlib.Path(args[0]).resolve()
    date = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--date=")),
                "unknown date")
    pages = topics(board)
    rows, tot = rollup(pages)
    if "--json" in sys.argv:
        print(json.dumps(dict(measured=date, board=board.name, rows=rows,
                              totals=dict(tot)), indent=2))
    else:
        print(render(rows, tot, date, board.name))
